import requests
from bs4 import BeautifulSoup

def extract_hrefs_colonne_pays(url):
    try:
        # Récupération du contenu HTML de la page
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Recherche des balises <li class="colonne_pays">
        li_elements = soup.find_all('li', class_='colonne_pays')

        # Extraction des href dans les balises <a>
        hrefs = []
        for li in li_elements:
            a_tag = li.find('a', href=True)
            if a_tag:
                hrefs.append(a_tag['href'])

        return hrefs

    except requests.RequestException as e:
        print(f"Erreur lors de la récupération de l'URL : {e}")
        return []


OUTPUT_FILE = "urls_diplomatie_gouv.csv"

with open(OUTPUT_FILE, "w", encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile)
    urls_diplomatie = extract_hrefs_colonne_pays("https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/")
    for url in urls_diplomatie:
        writer.writerow([f"https://www.diplomatie.gouv.fr/{url}" ])
