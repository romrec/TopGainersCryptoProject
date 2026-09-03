# TopGainersCryptoProject

## 📌 Description

**TopGainersCryptoProject** est une application de **veille crypto en temps réel** qui identifie les cryptomonnaies les plus performantes sur 24h. Elle combine une interface web **Streamlit**, un stockage **PostgreSQL**, un monitoring **Prometheus/Grafana** et un déploiement automatisé sur **AWS** (Free Tier) via **Terraform** et **GitHub Actions**.

---

## 🏗️ Stack technique complète

| Couche | Technologie | Rôle |
|--------|-------------|------|
| **Frontend** | Streamlit (Python) | Interface web interactive (port 8501) |
| **Backend** | Python 3.9 | Logique métier (app.py, top_movers.py, db.py) |
| **Base de données** | PostgreSQL 16 (alpine) | Stockage persistant des données crypto (port 5432) |
| **Monitoring** | Prometheus + Grafana | Collecte de métriques (port 9090) + dashboards (port 3000) |
| **Métriques app** | Prometheus client | Endpoint `/metrics` (port 8000) |
| **Conteneurisation** | Docker + Docker Compose | Orchestration des services |
| **CI/CD** | GitHub Actions | Tests + build multi-arch + push GHCR + déploiement |
| **Infrastructure** | Terraform (AWS) | Déploiement EC2 t3.micro (Free Tier) |
| **Kubernetes** | k3s (manifests) | Déploiement alternatif sur cluster k3s |

---

## 🚀 Démarrage rapide

### 1. Installation locale (Docker Compose)
```bash
git clone https://github.com/romrec/TopGainersCryptoProject.git
cd TopGainersCryptoProject
echo "DB_PASSWORD=change_me" > .env
docker compose up -d --build
```

### 2. Déploiement sur AWS (Terraform)
```bash
cd terraform-aws
cp terraform.tfvars.example terraform.tfvars
# Remplir les variables dans terraform.tfvars :
#   - region : Région AWS (ex: eu-west-3)
#   - my_ip : Votre IP publique (pour SSH)
#   - ssh_public_key_path : Chemin vers votre clé SSH publique

AWS_PROFILE=topgainers terraform init
AWS_PROFILE=topgainers terraform plan
AWS_PROFILE=topgainers terraform apply -auto-approve
```

### 3. Accès à l'application
Après le déploiement, récupérez l'IP publique avec :
```bash
AWS_PROFILE=topgainers terraform output instance_public_ip
```

- **Application Streamlit** : `http://<IP_PUBLIQUE>:8501`
- **Prometheus** : `http://<IP_PUBLIQUE>:9090`
- **Grafana** : `http://<IP_PUBLIQUE>:3000` (identifiants par défaut : admin/admin)
- **SSH** : `ssh -i ~/.ssh/id_rsa ubuntu@<IP_PUBLIQUE>` (depuis votre IP uniquement)

---

## 🧩 Architecture détaillée

### 1. Application (Streamlit)
- **app.py** : Interface web interactive (Streamlit) qui affiche les 10 meilleures cryptomonnaies
- **top_movers.py** : Récupère les données depuis l'API CoinGecko
- **db.py** : Couche d'accès aux données (PostgreSQL)
- **logging_conf.py** : Configuration des logs + métriques Prometheus

### 2. Base de données (PostgreSQL)
- **PostgreSQL 16** (image `postgres:16-alpine`)
- **Volume persistant** : `pg_data` (Docker) ou `postgres-pvc` (K8s)
- **Table `top_movers`** : stocke les symboles, prix, volumes, variations 24h

### 3. Monitoring (Prometheus + Grafana)
- **Prometheus** : scrape les métriques de l'app toutes les 10s (port 9090)
- **Grafana** : dashboards provisionnés automatiquement (port 3000)
- **Alertes** : règles dans `prometheus/alert_rules.yml`

### 4. CI/CD (GitHub Actions)
```
push sur main → [test (pytest)] → [build Docker GHCR] → [deploy SSH → EC2]
```
- **CI** : tests unitaires (pytest + PostgreSQL service)
- **Build** : build multi-arch Docker (amd64/arm64) + push sur `ghcr.io`
- **Deploy** : SSH sur EC2 → pull image → redémarre conteneurs

### 5. Infrastructure (Terraform AWS)
- **Instance** : `t3.micro` (1 vCPU / 1 Go RAM) — Free Tier
- **EBS** : 20 Go (gp3) — configuré dans `main.tf`
- **Swap** : 2 Go (créé par `user_data.sh`)
- **Security Group** : ports 22 (SSH), 8501 (app), 9090 (Prometheus), 3000 (Grafana)

---

## 🧩️ Kubernetes (k3s)

Le dossier `k8s/` contient les manifests Kubernetes pour déployer l'application sur un cluster **k3s** (Kubernetes léger).

### Ressources K8s

| Fichier | Description |
|---------|-------------|
| `namespace.yaml` | Namespace `topgainers` |
| `postgres-secret.yaml` | Secret contenant les identifiants PostgreSQL |
| `postgres-pvc.yaml` | Volume persistant pour PostgreSQL (10 Go) |
| `postgres-deployment.yaml` | Déploiement PostgreSQL 16 |
| `postgres-service.yaml` | Service interne PostgreSQL (ClusterIP) |
| `app-deployment.yaml` | Déploiement de l'application Streamlit |
| `app-service.yaml` | Service NodePort exposant l'application (30001) et les métriques (30002) |

### Déploiement K8s

```bash
kubectl apply -f k8s/
```

Ou fichier par fichier :
```bash
kubectl apply -f namespace.yaml
kubectl apply -f postgres-secret.yaml
kubectl apply -f postgres-pvc.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f postgres-service.yaml
kubectl apply -f app-deployment.yaml
kubectl apply -f app-service.yaml
```

### Vérification K8s

```bash
kubectl get pods -n topgainers
kubectl get svc -n topgainers
```

### Accès K8s

- **Application** : `http://<IP_VM>:30001`
- **Métriques Prometheus** : `http://<IP_VM>:30002/metrics`

### Notes K8s

- **PostgreSQL** est exposé uniquement en interne (ClusterIP) — pas accessible depuis l'extérieur
- **L'application** est exposée via NodePort (30001 pour Streamlit, 30002 pour les métriques)
- Le mot de passe PostgreSQL est dans le Secret `postgres-secret` (à changer en production)

---

## 🧪 Tests

```bash
python -m pytest tests/ -v
# tests spécifiques
python -m pytest tests/test_top_movers.py -v
python -m pytest tests/test_database.py -v
```

---

## 🔐 Sécurité

- SSH restreint à votre IP publique uniquement
- Pas de mot de passe, uniquement clé SSH
- Les secrets sont stockés dans les GitHub Secrets
- Le mot de passe PostgreSQL par défaut est `change_me` (à changer en production)
- Le fichier `terraform.tfvars` contient des secrets et est gitignoré

---

## 📁 Structure du projet

```
TopGainersCryptoProject/
├── .gitignore
├── app.py
├── db.py
├── top_movers.py
├── logging_conf.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── docker-compose.app.yml
├── docker-compose.monitoring.yml
├── prometheus.yml
├── prometheus/alert_rules.yml
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       │   └── prometheus.yml
│       └── dashboards/
│           ├── dashboards.yml
│           └── topgainers-dashboard.json
├── .github/
│   └── workflows/
│       └── docker.yml
├── terraform-aws/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── terraform.tfvars
│   ├── terraform.tfvars.example
│   ├── user_data.sh
│   └── README.md
├── k8s/
│   ├── namespace.yaml
│   ├── postgres-secret.yaml
│   ├── postgres-pvc.yaml
│   ├── postgres-deployment.yaml
│   ├── postgres-service.yaml
│   ├── app-deployment.yaml
│   ├── app-service.yaml
│   └── README.md
└── README.md
```

---

## 📊 Surveillance

- Interface Streamlit : http://localhost:8501 (local) ou http://<IP>:8501 (AWS)
- Métriques Prometheus : http://localhost:8000/metrics (local) ou http://<IP>:9090 (AWS)
- UI Prometheus : http://localhost:9090 (local) ou http://<IP>:9090 (AWS)
- Dashboard Grafana : http://localhost:3000 (local) ou http://<IP>:3000 (AWS)

---

## 💰 Coût

- **Instance EC2** : `t3.micro` (Free Tier 750h/mois)
- **EBS** : 20 Go (gp3) — inclus dans le Free Tier (30 Go)
- **Data transfert** : 15 Go/mois (inclus)
- **Total** : **0 €/mois** (sous le Free Tier)