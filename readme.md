# GENOVA – Guide Touristique Intelligent avec RAG

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
├── data/                          # Contient les fichiers de liens extraits depuis différents sites sources  
│   ├── urls_routard.csv              # Liste des URLs extraites depuis le site du Routard  
│   ├── urls_diplomatie_gouv.csv      # Liste des URLs extraites depuis le site du Ministère des Affaires étrangères  
│   └── urls_wikivoyage.csv           # Liste des URLs extraites depuis le site Wikivoyage  
│
├── evaluation/                   # Contient les scripts liés à l’évaluation des performances du système RAG  
│   └── RAG_LO17_evaluation.py       # Script d’évaluation des performances (métriques de pertinence, qualité des réponses, etc.)  
│  
├── .env                          # Fichier de configuration pour stocker les variables d’environnement (API keys, chemins, etc.)  
│  
├── index/                        # Contient les scripts liés à l’indexation et au moteur de recherche  
│   ├── chroma_index.py              # Script principal de création et d’interrogation de l’index Chroma (vecteurs, documents)  
│   └── documents.py                # Préparation, nettoyage et structuration des documents avant indexation  
│    
├── url_extraction/              # Contient les scripts d’extraction de données depuis les différentes sources en ligne  
│   ├── diplomatie_gouv.py          # Extraction des URLs et contenus depuis diplomatie.gouv.fr  
│   ├── routard.py                  # Extraction des URLs et contenus depuis le site du Routard  
│   └── wikivoyage.py               # Extraction des URLs et contenus depuis Wikivoyage  
│  
├── .gitignore                   # Liste des fichiers et dossiers à exclure du suivi Git  
├── app.py                       # Script principal de l’application Streamlit (interface utilisateur)    
├── LO17_Slides_RAG.pdf          # Support de présentation utilisé lors de la soutenance du projet   
├── LO17_Rapport_RAG.pdf          # Rapport de projet    
├── requirements.txt             # Liste des bibliothèques Python nécessaires au bon fonctionnement du projet  
├── readme.md                    # Documentation du projet : objectifs, instructions d’installation, usage  
└── demo_streamlit_genova.webm   # Vidéo de démonstration de l’application (fonctionnement en conditions réelles)  

## Évaluation du code

Enfin, pour assurer un code propre, lisible et conforme aux bonnes pratiques, nous avons utilisé l’outil `pylint` afin d’analyser l’ensemble de notre base de code. Grâce à ce travail, nous avons obtenu un score global supérieur à **10 / 10**, ce qui témoigne d’un code bien structuré, bien documenté et maintenable.


![image](https://github.com/user-attachments/assets/6fd152ac-8f0c-44b8-be91-b3837c1df397)


La commande utilisée pour obtenir ce score est la suivante :

```bash
pylint --disable=C0301,E0611,E1101 ./*.py

```


## Accès direct

L'application est disponible en ligne à l'adresse :  
[https://genova-rag.streamlit.app/](https://genova-rag.streamlit.app/)

### Remarque importante
L'application repose sur une base de données volumineuse (~2 Go).
En cas d’erreur du type :

**gdown.exceptions.FileURLRetrievalError
(This app has encountered an error...)**

cela signifie que la limite de téléchargement du lien Google Drive a été atteinte ; il suffit alors simplement de réessayer plus tard.

## Auteurs
Projet réalisé par :

- Samuel Beziat
- Emma Choukroun
- Jeanne Galet
- Selima Khessairi
