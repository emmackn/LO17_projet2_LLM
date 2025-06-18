"""
Script de crawling des URLs de guides sur Routard à partir d'une URL de départ.
Explore récursivement les liens internes vers les pages de guide.
"""

import requests
import csv
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from queue import Queue


def crawl_routard_guide_urls(start_url):
    target_prefix = "https://www.routard.com/fr/guide/"
    visited = set()
    to_visit = Queue()
    guide_urls = set()

    to_visit.put(start_url)
    headers = {"User-Agent": "Mozilla/5.0"}

    while not to_visit.empty():
        current_url = to_visit.get()

        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            response = requests.get(current_url, headers=headers, timeout=10)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            for link_tag in soup.find_all("a", href=True):
                href = link_tag["href"]
                full_url = urljoin(current_url, href).split("#")[0].split("?")[0]

                if full_url.startswith(target_prefix) and full_url not in visited:
                    to_visit.put(full_url)
                    guide_urls.add(full_url)

        except Exception as e:
            print(f"Erreur lors de la récupération de {current_url} : {e}")
            continue

    return sorted(guide_urls)


if __name__ == "__main__":
    start_url = "https://www.routard.com/fr/guide/c/europe"
    urls = crawl_routard_guide_urls(start_url)

    print(f"Total trouvé : {len(urls)} URLs")

    OUTPUT_FILE = "../data/urls_routard.csv"
    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        for url in urls:
            writer.writerow([url])
