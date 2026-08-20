# TopGainersCryptoProject

## Description
Ce projet fournit des outils pour identifier les cryptomonnaies les plus performantes sur 24 h, avec une interface web Streamlit, du stockage PostgreSQL, du monitoring Prometheus/Grafana et des tests unitaires. Déploiement sur **Amazon Web Services (AWS)**.

## Fonctionnalités
- Affichage en temps réel des 10 meilleures cryptomonnaies (gain sur 24 h)
- Interface web simple avec Streamlit
- Stockage persistant des données en PostgreSQL
- Métriques exposées à Prometheus (port 8000)
- Interface Grafana avec dashboards provisionnés automatiquement
- Alertes Prometheus (règles d'alerte)
- Support Docker (docker-compose) et Kubernetes (k3s)
- Tests unitaires complets
- Déploiement automatisé via GitHub Actions

## Installation

### Prérequis
- Python 3.9+
- Git
- Compte AWS avec accès Free Tier
- Docker et Docker Compose
- Terraform 1.5+
- AWS CLI configuré

### Installation locale (Docker Compose)
```bash
git clone https://github.com/romrec/TopGainersCryptoProject.git
cd TopGainersCryptoProject
echo "DB_PASSWORD=change_me" > .env
docker compose up -d --build
```

### Déploiement sur AWS (Terraform)

#### Infrastructure Terraform
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

#### Accès à l'application
Après le déploiement, récupérez l'IP publique avec :
```bash
AWS_PROFILE=topgainers terraform output instance_public_ip
```

- **Application Streamlit** : `http://<IP_PUBLIQUE>:8501`
- **Prometheus** : `http://<IP_PUBLIQUE>:9090`
- **Grafana** : `http://<IP_PUBLIQUE>:3000` (identifiants par défaut : admin/admin)
- **SSH** : `ssh -i ~/.ssh/id_rsa ubuntu@<IP_PUBLIQUE>` (depuis votre IP uniquement)

#### Secrets GitHub requis
Pour le déploiement automatisé, configurez ces secrets dans votre dépôt GitHub
(Paramètres GitHub → Secrets and variables → Actions) :
- **`EC2_HOST`** : IP publique de l'instance EC2
- **`SSH_PRIVATE_KEY`** : Clé privée SSH pour se connecter à l'instance

Récupérez l'IP après `terraform apply` :
```bash
AWS_PROFILE=topgainers terraform output instance_public_ip
```

#### Workflow GitHub Actions
Le déploiement est **entièrement automatisé** via GitHub Actions :
- **CI** (sur chaque push/PR) : tests unitaires (pytest + PostgreSQL service)
- **Build** (après tests) : build multi-arch Docker (amd64/arm64) + push sur `ghcr.io`
- **Deploy** (sur push vers `main`) : SSH sur EC2 → pull image → redémarre conteneurs

```
push sur main → [test] → [build → GHCR] → [deploy → EC2]
```

La construction Docker se fait sur GitHub Actions (`ubuntu-latest`, plus rapide que t3.micro).
L'instance EC2 **pull** l'image depuis GHCR — aucun build local nécessaire !

### Tests
```bash
python -m pytest tests/ -v
# tests spécifiques
python -m pytest tests/test_top_movers.py -v
python -m pytest tests/test_database.py -v
```

## Surveillance
- Interface Streamlit : http://localhost:8501 (local) ou http://<IP>:8501 (AWS)
- Métriques Prometheus : http://localhost:8000/metrics (local) ou http://<IP>:9090 (AWS)
- UI Prometheus : http://localhost:9090 (local) ou http://<IP>:9090 (AWS)
- Dashboard Grafana : http://localhost:3000 (local) ou http://<IP>:3000 (AWS)

## Architecture
```
┌─────────────────────────────────────────────────────────┐
│                    Instance EC2 (t3.micro)               │
│                    1 vCPU / 1 GB RAM (Free Tier)         │
│                    Ubuntu 22.04 + Swap 2 Go              │
└─────────────────────────────────────────────────────────┘
  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐
  │  Streamlit  │  │  PostgreSQL  │  │  Prometheus  │  │ Grafana  │
  │  app.py     │  │  db.py       │  │  :9090       │  │ :3000   │
  │  :8501      │  │  :5432       │  │  metrics:8000│  │ dash   │
  └─────────────┘  └──────────────┘  └──────────────┘  └──────────┘
       │                  │                  │                │
       └──────────────────┴──────────────────┴────────────────┘
                           Docker Compose
```

## Sécurité
- SSH restreint à votre IP publique uniquement
- Pas de mot de passe, uniquement clé SSH
- Les secrets sont stockés dans les GitHub Secrets
- Le mot de passe PostgreSQL par défaut est `change_me` (à changer en production)
- Le fichier `terraform.tfvars` contient des secrets et est gitignoré

## Structure du projet
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
│   ├── provisioning/
│   │   ├── datasources/
│   │   │   └── prometheus.yml
│   │   └── dashboards/
│   │       └── dashboards.yml
│   └── dashboards/
│       └── topgainers-dashboard.json
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
