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