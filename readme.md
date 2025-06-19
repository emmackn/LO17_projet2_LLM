# GENOVA – Guide Touristique Intelligent avec RAG et LLM

Projet réalisé dans le cadre du module **LO17 – Indexation et Recherche d’Information (UTC)**.

---

## Objectif du projet

**GENOVA** (Générateur de réponses touristiques avec navigation assistée) est une application de type **RAG** (Retrieval-Augmented Generation) combinant :
- extraction de contenus touristiques,
- indexation sémantique,
- génération de réponses à l’aide d’un LLM (Gemini),
- et une interface simple via **Streamlit**.

Elle permet de répondre à des requêtes du type :
- « Que faire à Tokyo ? »
- « Quels sont les plats typiques de Naples ? »
- « Quel est le climat en Albanie ? »

---
## Technologies principales

- **LangChain** pour la gestion du pipeline RAG
- **Gemini** (Google) pour les embeddings et la génération
- **ChromaDB** pour le stockage vectoriel
- **Streamlit** pour l’interface utilisateur
- **RAGAS** pour l’évaluation automatique des réponses

---
## Structure du projet

LO17_projet2_LLM/  
├── data/ # Dossier des données  
│ ├── bdd/ # Base de données  
│ └── documents/ # Documents analysés  
├── src/  
│ ├── app.py # Script principal de l'application  
│ ├── urls_extraction.py # Extraction d'URLs  
│ └── index.py # Indexation des données  
├── .env # Variables d'environnement  
├── .gitignore # Fichiers ignorés par Git  
├── requirements.txt # Dépendances Python  
└── demo_streamlit_genova.webm # Démo vidéo de l'application  

## Accès direct

L'application est disponible en ligne à l'adresse :  
[https://genova-rag.streamlit.app/](https://genova-rag.streamlit.app/)


## Auteurs
Projet réalisé par :

- Samuel Beziat
- Emma Choukroun
- Jeanne Galet
- Selima Khessairi
