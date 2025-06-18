"""
Script d'indexation de documents dans une base vectorielle Chroma en utilisant les embeddings Google Gemini.
Utilise un système de checkpoint pour reprendre en cas d'interruption.
"""

import os
import json
import pickle
import time
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

BATCH_SIZE = 10
PERSIST_DIR = "../data/chroma_db"
CHECKPOINT_FILE = "../data/checkpoint.json"
GOOGLE_API_KEY = "AIzaSyCQZT0srA1PeWrYnXOJP6rA1c8remXbgcM"


def load_documents(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def get_start_batch():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE, "r") as f:
            checkpoint = json.load(f)
            return checkpoint.get("last_batch", 0)
    return 0


def save_checkpoint(batch_index):
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump({"last_batch": batch_index + 1}, f)


if __name__ == "__main__":
    all_docs = load_documents("../data/docs_rag.pkl")
    total_docs = len(all_docs)
    print(f"Nb de documents: {total_docs}")

    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

    vectorstore = Chroma(
        embedding_function=embedding_model,
        persist_directory=PERSIST_DIR
    )

    start_batch = get_start_batch()

    try:
        for batch_index in range(start_batch, (total_docs // BATCH_SIZE) + 1):
            time.sleep(1)
            start = batch_index * BATCH_SIZE
            end = min(start + BATCH_SIZE, total_docs)
            raw_batch_docs = all_docs[start:end]

            if not raw_batch_docs:
                break

            # Filtre les documents n'ayant aucun contenu
            batch_docs = [
                doc for doc in raw_batch_docs
                if doc.page_content.strip() != ""
            ]

            if not batch_docs:
                print(f"Batch {batch_index} ignoré : aucun document valide")
                continue

            print(f"Processing batch {batch_index} ({start} to {end}) avec {len(batch_docs)} documents valides...")

            vectorstore.add_documents(batch_docs)
            save_checkpoint(batch_index)

    except Exception as e:
        print(f"Erreur lors de l'indexation : {e}")
        print(f"Relancez à partir du batch {batch_index}")
