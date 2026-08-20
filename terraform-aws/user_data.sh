#!/bin/bash
set -e

# Mise à jour du système
apt-get update -y
apt-get upgrade -y

# Installation de Docker
apt-get install -y docker.io docker-compose-v2 git curl

# Démarrage de Docker
systemctl enable docker
systemctl start docker
usermod -aG docker ubuntu

# Création d'un swap file (2 Go) - essentiel sur t3.micro (1 Go RAM)
echo "=== CRÉATION DU SWAP FILE ==="
if [ ! -f /swapfile ]; then
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "Swap file de 2 Go créé et activé"
else
    echo "Swap file déjà existant"
fi

# Optimisation sysctl pour faible mémoire
echo "=== OPTIMISATION SYSCTL ==="
cat >> /etc/sysctl.conf << 'EOF'
# Optimisations pour t3.micro (1 Go RAM)
vm.swappiness=10
vm.vfs_cache_pressure=50
vm.overcommit_memory=1
EOF
sysctl -p

# Clonage du projet
mkdir -p /opt/topgainers
cd /opt/topgainers
git clone https://github.com/romrec/TopGainersCryptoProject.git .

# Configuration du mot de passe DB
echo "DB_PASSWORD=change_me" > .env

# Démarrage de la base de données en premier
docker compose up -d db

# Attendre que PostgreSQL soit prêt (healthcheck)
echo "=== ATTENTE DE LA BASE DE DONNÉES ==="
for i in $(seq 1 30); do
    if docker compose exec -T db pg_isready -U postgres 2>/dev/null; then
        echo "PostgreSQL est prêt"
        break
    fi
    echo "En attente de PostgreSQL... ($i/30)"
    sleep 2
    if [ $i -eq 30 ]; then
        echo "ERREUR: PostgreSQL n'est pas devenu prêt dans le délai imparti"
        docker compose logs db
        exit 1
    fi
done

# Démarrage des services de monitoring (Prometheus + Grafana)
docker compose up -d prometheus grafana

# Attendre que Prometheus et Grafana soient prêts
echo "=== ATTENTE DE PROMETHEUS ET GRAFANA ==="
for i in $(seq 1 15); do
    PROM=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:9090/-/healthy 2>/dev/null || echo "000")
    GRAF=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/health 2>/dev/null || echo "000")
    echo "Prometheus: $PROM, Grafana: $GRAF"
    if [ "$PROM" = "200" ] && [ "$GRAF" = "200" ]; then
        echo "Prometheus et Grafana sont prêts"
        break
    fi
    sleep 2
    if [ $i -eq 15 ]; then
        echo "ATTENTION: Prometheus ou Grafana n'est pas prêt, démarrage de l'app quand même"
    fi
done

# Démarrage de l'application (image pullée depuis GHCR)
docker compose pull top-gainers-crypto
docker compose up -d top-gainers-crypto

# Diagnostic : vérifier l'état des conteneurs
echo "=== ÉTAT DES CONTENEURS ==="
docker compose ps

# Vérifier l'utilisation mémoire
echo "=== UTILISATION MÉMOIRE ==="
free -h
docker stats --no-stream

# Vérifier si Grafana est bien en écoute sur le port 3000
echo "=== VÉRIFICATION GRAFANA ==="
docker compose logs grafana --tail=30 2>&1 || true

# Vérifier si l'application est bien en écoute sur le port 8501
echo "=== VÉRIFICATION APPLICATION ==="
docker compose logs top-gainers-crypto --tail=30 2>&1 || true

# Vérifier les métriques Prometheus
echo "=== VÉRIFICATION MÉTRIQUES PROMETHEUS ==="
curl -s http://localhost:8000/metrics 2>&1 | head -20 || true

echo "Déploiement terminé"