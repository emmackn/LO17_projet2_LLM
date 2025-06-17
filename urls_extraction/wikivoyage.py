import mwxml
import csv


def sluggify_name_wikivoyage(name):
    return name.replace(" ", "_").replace("'", "%27")


DUMP_FILE = "frwikivoyage-20250520-pages-articles-multistream.xml"
OUTPUT_FILE = "urls_wikivoyage.csv"

with open(OUTPUT_FILE, "w", encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile)

    dump = mwxml.Dump.from_file(open(DUMP_FILE, 'rb'))
    for page in dump:
        if page.namespace != 0:
            continue

        page_title = sluggify_name_wikivoyage(page.title)
        url_article = f"https://fr.wikivoyage.org/wiki/{page_title}"
        writer.writerow([url_article])