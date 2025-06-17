import csv
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
from collections import deque
from concurrent.futures import ThreadPoolExecutor

REGIONS = [
    "france",
    "europe",
    "amerique",
    "afrique",
    "asie",
    "moyen-orient",
    "oceanie-pacifique",
    "antarctique",
]

BASE_URL = "https://www.lonelyplanet.fr/destinations"
TARGET_PREFIX_BASE = "https://www.lonelyplanet.fr/destinations"


def crawl_region(region):
    start_url = f"{BASE_URL}"
    target_prefix = f"{TARGET_PREFIX_BASE}/{region}"

    visited = set()
    to_visit = deque([start_url])
    destination_urls = set()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.lonelyplanet.fr"
    }

    while to_visit:
        print(region, len(to_visit), len(destination_urls))
        current_url = to_visit.popleft()

        if current_url in visited:
            continue
        visited.add(current_url)

        try:
            response = requests.get(current_url, headers=headers, timeout=15)
            if response.status_code != 200:
                print(f"[{region}] Erreur {response.status_code} sur {current_url}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            for link_tag in soup.find_all("a", href=True):
                href = link_tag["href"]
                full_url = urljoin(current_url, href).split("#")[0].split("?")[0]

                if full_url.startswith(target_prefix) and full_url not in visited and full_url not in to_visit:
                    destination_urls.add(full_url)
                    to_visit.append(full_url)

            time.sleep(1)  # Pause entre les requêtes

        except Exception as e:
            print(f"[{region}] Erreur sur {current_url}: {e}")
            continue

    return destination_urls


def crawl_all_regions_parallel():
    all_urls = set()
    with ThreadPoolExecutor(max_workers=len(REGIONS)) as executor:
        futures = {executor.submit(crawl_region, region): region for region in REGIONS}
        for future in futures:
            try:
                urls = future.result()
                all_urls.update(urls)
            except Exception as e:
                region = futures[future]
                print(f"Erreur dans la région {region}: {e}")
    return sorted(all_urls)


# Lancer le crawl
all_urls = crawl_all_regions_parallel()

# Écriture CSV
OUTPUT_FILE = "urls_lonelyplanet.csv"
with open(OUTPUT_FILE, "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f)
    for url in all_urls:
        writer.writerow([url])

print(f"\n✅ Terminé : {len(all_urls)} URLs enregistrées dans {OUTPUT_FILE}")
