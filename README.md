# TopGainersCryptoProject

## Description
Ce projet fournit des outils pour identifier les cryptomonnaies les plus performantes sur 24 h, avec une interface web Streamlit, du stockage SQLite, du monitoring Prometheus et des tests unitaires.

## Fonctionnalités
- Affichage en temps réel des 10 meilleures cryptomonnaies (gain sur 24 h)
- Interface web simple avec Streamlit
- Stockage persistant des données en SQLite
- Métriques exposées à Prometheus
- Support Docker
- Tests unitaires complets

## Installation

### Prérequis
- Python 3.9+
- Git

### Démarrage rapide
```bash
git clone https://github.com/romrec/TopGainersCryptoProject.git
cd TopGainersCryptoProject
pip install -r requirements.txt
streamlit run app.py
```

### Avec Docker
```bash
docker build -t top-gainers-crypto .
docker run -p 8501:8501 top-gainers-crypto
```

## Utilisation

### Développement local
```bash
streamlit run app.py
# ou avec rechargement à chaud
streamlit run app.py --server.headless false
```

### Docker Compose
```bash
docker-compose up -d
# arrêter
docker-compose down
```

## Monitoring
- Interface Streamlit : http://localhost:8501
- Métriques Prometheus : http://localhost:8000/metrics
- UI Prometheus : http://localhost:9090

## CI/CD – Pipeline DevSecOps
Un **pipeline DevSecOps** a été ajouté pour automatiser les contrôles de sécurité, la construction et le déploiement. Le fichier de workflow se trouve à `.github/workflows/devsecops.yml` et s’exécute à chaque push sur les branches `main` ou `develop` ainsi que sur les pull‑requests.

### Étapes du pipeline
1. **SAST** – Analyse statique du code avec **Snyk Code** (génère un rapport SARIF).
2. **SCA** – Analyse des dépendances avec **Snyk Open Source**.
3. **Build** – Construction de l’image Docker (`docker build -t myapp:${{ github.sha }}`).
4. **DAST** – Scan dynamique avec **OWASP ZAP** sur l’URL de staging.

### Déclencher le pipeline
Poussez un commit sur `main` ou `develop`, ou ouvrez une pull‑request. Vous pouvez suivre l’exécution dans l’onglet **Actions** du dépôt.

### Prochaines étapes
- Ajouter les identifiants du registre Docker comme secrets GitHub (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`, etc.) et étendre le workflow pour pousser l’image.
- Remplacer l’étape de déploiement placeholder par votre script de déploiement réel.

## Environnement de test (branche `dev`)

Un environnement de test complet, dissocié de la prod, est disponible sur la branche `dev`.

### Fichiers de test
```
TopGainersCryptoProject/
├── test/
│   ├── app_test.py               # Application avec données mockées
│   ├── Dockerfile.test           # Dockerfile dédié au test
│   └── docker-compose.test.yml   # Compose pour l'environnement test
└── data-test/                    # Volume de données test (isolé)
```

### Lancer l'environnement de test
```bash
# Basculer sur la branche dev
git checkout dev

# Lancer les services de test
docker compose -f test/docker-compose.test.yml up

# Accès
# - Interface Streamlit : http://localhost:8502
# - Métriques Prometheus : http://localhost:8001/metrics
```

### Différences avec la prod

| Caractéristique | Prod (main) | Test (dev) |
|---|---|---|
| API CoinGecko | Réelle | Données mockées (10 crypto factices) |
| Port Streamlit | 8501 | 8502 |
| Port Prometheus | 8000 | 8001 |
| Base de données | `data/crypto_data.db` | `data-test/test.db` |
| Commande | `docker compose up` | `docker compose -f test/docker-compose.test.yml up` |

## Tests
```bash
python -m unittest discover tests -v
# tests spécifiques
python -m unittest tests.test_top_movers -v
python -m unittest tests.test_database -v
```

## Structure du projet
```
TopGainersCryptoProject/
├── .github/
│   └── workflows/
│       └── devsecops.yml   # CI/CD GitHub Actions pour DevSecOps
├── app.py
├── db.py
├── docker-compose.yml
├── Dockerfile
├── logging_conf.py
├── requirements.txt
├── top_movers.py
├── tests/
│   ├── test_database.py
│   └── test_top_movers.py
└── README.md
```