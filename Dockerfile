# Utilise une image Python officielle
FROM python:3.9-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie requirements.txt et installe les dépendances
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie le reste du code de l'application
COPY . .

# Expose le port 8501 (port default de Streamlit)
EXPOSE 8501

# Commande à executer pour démarrer l'application
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
