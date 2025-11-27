#!/bin/bash

echo "Création du dossier projet..."
mkdir -p TopGainersCryptoProject
cd TopGainersCryptoProject

echo "Clonage du dépôt GitHub..."
git clone https://oauth2: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@github.com/romrec/TopGainersCryptoProject.git .

echo "Installation des dépendances..."
pip install --upgrade pip
pip install streamlit requests

echo "Lancement de l'application Streamlit..."
streamlit run app.py
