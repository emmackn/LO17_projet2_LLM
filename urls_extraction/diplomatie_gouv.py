"""
Script d'extraction des liens des fiches pays depuis la page Diplomatie.gouv et sauvegarde dans un fichier CSV.
"""

import requests
from bs4 import BeautifulSoup
import csv


def extract_hrefs_colonne_pays(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        li_elements = soup.find_all("li", class_="colonne_pays")
        return [li.find("a")["href"] for li in li_elements if li.find("a", href=True)]
    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de l'URL : {e}")
        return []


if __name__ == "__main__":
    OUTPUT_FILE = "..data/urls_diplomatie_gouv.csv"
    source_url = "https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/"
    urls_diplomatie = extract_hrefs_colonne_pays(source_url)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for url in urls_diplomatie:
            writer.writerow([f"https://www.diplomatie.gouv.fr/{url}"])
