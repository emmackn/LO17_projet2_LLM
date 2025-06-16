#!/bin/bash

# Installer localtunnel si pas encore installé
npm install -g localtunnel

# Créer le dossier pour logs s'il n'existe pas
mkdir -p /content

# Lancer Streamlit en arrière-plan et rediriger les logs
streamlit run app.py &> /content/logs.txt &

# Attendre un peu que Streamlit démarre (ajuste au besoin)
sleep 5

# Lancer localtunnel sur le port 8501
npx localtunnel --port 8501
