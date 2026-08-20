# Image Python officielle, version slim pour réduire la taille
FROM python:3.9-slim

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Installation des dépendances système (libpq5 nécessaire à psycopg2-binary)
RUN apt-get update && apt-get install -y libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copie et installation des dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source de l'application
COPY . .

# Création d'un utilisateur non-root sans mot de passe ni shell interactif
RUN adduser --disabled-password --gecos '' appuser \
    && mkdir -p /app/data /app/logs \
    && chown -R appuser:appuser /app

# Passage à l'utilisateur applicatif
USER appuser

# Déclaration du volume pour la persistance de la base de données
VOLUME ["/app/data"]

# Exposition des ports : 8501 pour Streamlit, 8000 pour Prometheus
EXPOSE 8501 8000

# Lancement de l'application
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]