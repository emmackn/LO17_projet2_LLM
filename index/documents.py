import pickle
import pandas as pd
from langchain.document_loaders import WebBaseLoader
from langchain.schema import Document
from concurrent.futures import ThreadPoolExecutor, as_completed
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


# Charger les fichiers CSV
urls_routard = pd.read_csv("../data/urls_routard.csv")
urls_wikivoyage = pd.read_csv("../data/urls_wikivoyage.csv")
urls_diplomatie = pd.read_csv("../data/urls_diplomatie_gouv.csv")
urls_lonely = pd.read_csv("../data/urls_lonelyplanet.csv")


# Fonction pour charger un seul document
def load_document(url):
    try:
        loader = WebBaseLoader(url)
        docs = loader.load()
        text_content = docs[0].page_content
        return Document(page_content=text_content, metadata={"source": url})
    except Exception as e:
        print(f"Erreur lors du chargement de la page {url}: {e}")
        return None


# Fonction pour charger les documents d'une liste d'URLs
def load_documents_from_urls(url_list):
    documents = []
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(load_document, url) for url in url_list]
        for future in as_completed(futures):
            doc = future.result()
            if doc:
                documents.append(doc)
    return documents

# Parallélisation sur les 4 sources
sources = {
    "routard": urls_routard.iloc[:, 0].tolist(),
    "wikivoyage_and_diplomatie": urls_wikivoyage.iloc[:, 0].tolist() + urls_diplomatie.iloc[:, 0].tolist(),
    "lonely": urls_lonely.iloc[:, 0].tolist()
}

results = {}

with ThreadPoolExecutor(max_workers=4) as executor:
    futures = {executor.submit(load_documents_from_urls, url_list): name for name, url_list in sources.items()}
    for future in as_completed(futures):
        source_name = futures[future]
        try:
            results[source_name] = future.result()
        except Exception as e:
            print(f"Erreur lors du traitement de {source_name} : {e}")
            results[source_name] = []

# Fusionner tous les documents
all_docs = results["routard"] + results["wikivoyage_and_diplomatie"] + results["lonely"]
with open("data/all_docs_lo17.pkl", "wb") as f:
    pickle.dump(all_docs, f, protocol=pickle.HIGHEST_PROTOCOL)