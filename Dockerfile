# Utilise une image Python officielle
FROM python:3.9-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie requirements.txt et installe les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code de l'application
COPY . .

# Crée un volume pour persister la DB et les logs
VOLUME ["/app/data"]

# Expose le port 8501 (port default de Streamlit) et 8000 (Prometheus)
EXPOSE 8501 8000

# Commande à executer pour démarrer l'application (Prometheus démarre automatiquement dans l'app)
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
