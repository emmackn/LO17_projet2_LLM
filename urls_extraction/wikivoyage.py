"""
Script de génération des URLs des articles Wikivoyage à partir d'un dump XML bz2.
Le fichier bz2 est d'abord décompressé puis analysé pour extraire les titres des pages principales (namespace 0).
"""

import mwxml
import csv
import bz2
import shutil
import os


def sluggify_name_wikivoyage(name):
    return name.replace(" ", "_").replace("'", "%27")


def decompress_bz2(input_path, output_path):
    with bz2.open(input_path, "rb") as f_in, open(output_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


if __name__ == "__main__":
    DUMP_BZ2 = "../data/frwikivoyage-20250520-pages-articles-multistream.xml.bz2"
    DUMP_XML = "../data/frwikivoyage-20250520-pages-articles-multistream.xml"
    OUTPUT_FILE = "../data/urls_wikivoyage.csv"

    if not os.path.exists(DUMP_XML):
        print("Décompression du fichier .bz2...")
        decompress_bz2(DUMP_BZ2, DUMP_XML)

    with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        dump = mwxml.Dump.from_file(open(DUMP_XML, "rb"))

        for page in dump:
            if page.namespace != 0:
                continue
            page_title = sluggify_name_wikivoyage(page.title)
            url_article = f"https://fr.wikivoyage.org/wiki/{page_title}"
            writer.writerow([url_article])
