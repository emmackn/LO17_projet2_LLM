import os
import json
from langchain_community.vectorstores import Chroma
import pickle
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import time

with open("docs_rag.pkl", "rb") as f:
    all_docs = pickle.load(f)

# GOOGLE_API_KEY = "AIzaSyAdzaU5i8Iy0Q7il_Do2T4m-75-l819cZ0"
GOOGLE_API_KEY = "AIzaSyCQZT0srA1PeWrYnXOJP6rA1c8remXbgcM"
BATCH_SIZE = 10
PERSIST_DIR = "data/chroma_db"
CHECKPOINT_FILE = "data/checkpoint.json"

# Charger les documents
total_docs = len(all_docs)
print(f"Nb de documents: {total_docs}")
# Embedding model
gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
embedding_model = gemini_embeddings  # Votre modèle d'embedding

# Charger le checkpoint s'il existe
if os.path.exists(CHECKPOINT_FILE):
    with open(CHECKPOINT_FILE, "r") as f:
        checkpoint = json.load(f)
        start_batch = checkpoint.get("last_batch", 0)
else:
    start_batch = 0

# Initialiser ou recharger la base Chroma
vectorstore = Chroma(
    embedding_function=embedding_model,
    persist_directory=PERSIST_DIR
)

try:
    for batch_index in range(start_batch, (total_docs // BATCH_SIZE) + 1):
        time.sleep(1)
        start = batch_index * BATCH_SIZE
        end = min(start + BATCH_SIZE, total_docs)
        raw_batch_docs = all_docs[start:end]

        if not raw_batch_docs:
            break

        # Filtrer les documents valides
        batch_docs = [
            doc for doc in raw_batch_docs
            if doc.page_content.strip() != "" and "lonely" not in doc.metadata.get("source", "").lower()
        ]

        if not batch_docs:
            print(f"Batch {batch_index} ignoré : aucun document valide")
            continue

        print(f"Processing batch {batch_index} ({start} to {end}) avec {len(batch_docs)} documents valides...")

        # Ajouter et persister
        vectorstore.add_documents(batch_docs)

        # Sauvegarder le checkpoint
        with open(CHECKPOINT_FILE, "w") as f:
            json.dump({"last_batch": batch_index + 1}, f)

except Exception as e:
    print(f"Erreur lors de l'indexation : {e}")
    print(f"Relancez à partir du batch {batch_index}")
