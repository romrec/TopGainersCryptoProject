#!/bin/bash

echo "Installation des dépendances..."
pip install --upgrade pip
pip install streamlit requests

echo "Lancement de l'application Streamlit..."
streamlit run app.py
