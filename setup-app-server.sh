#!/bin/bash

echo "Création du dossier projet..."
mkdir -p TopGainersCryptoProject
cd TopGainersCryptoProject

echo "Clonage du dépôt GitHub..."

echo "Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Lancement de l'application Streamlit..."
streamlit run app.py

