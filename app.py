import os
import requests
import gdown
import zipfile
from dotenv import load_dotenv
from datetime import datetime
import streamlit as st
from langchain.chains import ConversationalRetrievalChain
from langchain import PromptTemplate
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Création du RAG
gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

gdrive_id = "1Oelj-dJWhUocrT_1DkAtApQlC3zKCxkB"
url = f"https://drive.google.com/uc?id={gdrive_id}"
zip_path = "chroma_db.zip"
gdown.download(url, zip_path, quiet=False)

extract_dir = "./"

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

vectorstore_disk = Chroma(
                        persist_directory="./chroma_db",       # Directory of db
                        embedding_function=gemini_embeddings   # Embedding model
                   )

# Initialisation du LLM Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3
)

# Utilisation du vectorstore_disk précédemment défini
retriever = vectorstore_disk.as_retriever(search_kwargs={"k": 5})

# Mémoire pour gérer l’historique de la conversation
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True  # Important pour Gemini
)

if "chat_history" in st.session_state and st.session_state.chat_history:
    for user_msg, ai_msg in st.session_state.chat_history:
        memory.chat_memory.add_user_message(user_msg)
        memory.chat_memory.add_ai_message(ai_msg)

# Prompt précis pour le comportement du modèle
prompt = PromptTemplate.from_template("""
Tu es un guide touristique expert. Ta tâche est de répondre à la question de l'utilisateur en t'appuyant uniquement sur les informations fournies dans le contexte.

Règles à respecter :
- Ne fais aucune inférence ou supposition. Reste strictement dans le cadre du contexte.
- N’ajoute aucun contenu promotionnel, suggestion, ou lien externe non mentionné explicitement.
- Si l'information n’est pas disponible dans le contexte, réponds clairement que tu ne sais pas.
- Rédige une réponse claire, concise et directement utile.
- Cite les URLs exactes des données que tu utilises.
- Ne cite pas la même URL plusieurs fois.

Format :
- Réponds de manière professionnelle.
- Évite les formules vagues ou incertaines.
- Si plusieurs lieux ou options sont possibles, liste-les.

Question : {question}
Contexte : {context}
Réponse :
""")

# Création de la chaîne de QA conversationnelle
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt}
)

### Interface Streamlit ###

st.set_page_config(
    page_title="Genova - Guide de Voyage IA",
    page_icon="🌍",
    layout="wide"
)

st.markdown("""
<style>
    body {
        background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .main {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 0 20px rgba(0,0,0,0.2);
    }
    .title {
        font-family: 'Trebuchet MS', sans-serif;
        font-size: 52px;
        font-weight: bold;
        color: #2c3e50;
    }
    .subtitle {
        font-family: 'Georgia', serif;
        font-size: 22px;
        font-style: italic;
        color: #34495e;
        margin-bottom: 2rem;
    }
    .chatbox {
        background-color: #fefefe;
        border-left: 5px solid #2980b9;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if st.sidebar.button("Nouveau chat"):
    st.session_state.chat_history = []
    if "temp_input" in st.session_state:
        del st.session_state["temp_input"]
    st.rerun()

st.sidebar.markdown("## Historique")
if st.session_state.chat_history:
    for i, (q, _) in enumerate(reversed(st.session_state.chat_history), 1):
        st.sidebar.markdown(f"{i}. {q}")
else:
    st.sidebar.markdown("Aucune question posée")

st.sidebar.markdown("---")
st.sidebar.markdown("## Exemples de questions")
example_questions = [
    "Que faire à Tokyo ?",
    "Quels sont les plats typiques de Naples ?",
    "Propose moi un itinéraire à Lisbonne",
    "Quel est le climat en Albanie ?",
    "Les plus beaux quartiers de Buenos Aires"
]
for q in example_questions:
    if st.sidebar.button(q):
        st.session_state.temp_input = q
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown(f"*{datetime.now().strftime('%A %d %B %Y')}*")

with st.container():
    st.markdown('<div class="title">Genova</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Votre compagnon de route, guide IA des voyageurs curieux</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.subheader("Posez votre question sur une destination")

    user_input = st.text_input(
        "Où voulez-vous aller ? Que voulez-vous savoir ?",
        key="temp_input"
    )

    if user_input:
        ai_response = qa_chain.invoke({"question": user_input})["answer"]

        st.session_state.chat_history.append((user_input, ai_response))
        del st.session_state["temp_input"]
        st.session_state.temp_input = ""
        st.rerun()

    for question, answer in reversed(st.session_state.chat_history):
        st.markdown(f"*Vous* : {question}")
        st.markdown(f"<div class='chatbox'><b>Genova :</b> {answer}</div>", unsafe_allow_html=True)