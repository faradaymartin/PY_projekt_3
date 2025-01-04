import requests
from bs4 import BeautifulSoup
import csv
import argparse
import sys

# Nastavení argumentů
parser = argparse.ArgumentParser(description='Scrapování dat z webu a ukládání do CSV souboru.')
parser.add_argument('url', type=str, help='Odkaz na územní celek, který chcete scrapovat')
parser.add_argument('output_file', type=str, help='Jméno výstupního souboru => vysledky_voleb.csv')
args = parser.parse_args()

# Kontrola argumentů
if not args.url.startswith("https://www.volby.cz/"):
    print("CHYBA: Neplatný odkaz. Ujisti se, že odkaz začíná 'https://www.volby.cz/'.")
    sys.exit(1)

if not args.output_file.endswith(".csv"):
    print("CHYBA: Neplatný název souboru. Ujistěte se, že název souboru končí '.csv'.")
    sys.exit(1)

url = args.url

print(f"STAHUJI DATA Z VYBRANÉHO URL: {url}")

# stránka
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Hledáme všechny odkazy na obce
obce_links = soup.find_all('a', href=True)

# Procházíme odkazy a sbíráme data
all_strany = set()
rows = []
for link in obce_links:
    if link.text.strip().isdigit():  # Nebereme v úvahu odkazy, které nejsou čísla obcí
        obec_url = "https://www.volby.cz/pls/ps2017nss/" + link['href']
        obec_response = requests.get(obec_url)
        obec_soup = BeautifulSoup(obec_response.content, 'html.parser')

        # Selekce dat o obcích
        kod_obce = link.text.strip()
        nazev_obce_elem = None
        for h3 in obec_soup.find_all('h3'):
            if "Obec:" in h3.text:
                nazev_obce_elem = h3
                break

        if nazev_obce_elem:
            nazev_obce = nazev_obce_elem.text.replace("Obec:", "").strip()
        else:
            nazev_obce = "N/A"

        volici_v_seznamu_elem = obec_soup.find('td', headers='sa2')
        vydane_obalky_elem = obec_soup.find('td', headers='sa3')
        platne_hlasy_elem = obec_soup.find('td', headers='sa6')

        if volici_v_seznamu_elem and vydane_obalky_elem and platne_hlasy_elem:
            volici_v_seznamu = volici_v_seznamu_elem.text.strip()
            vydane_obalky = vydane_obalky_elem.text.strip()
            platne_hlasy = platne_hlasy_elem.text.strip()

            # Selekce názvů stran a hlasů
            strany_hlasy = {}
            for strana in obec_soup.find_all('tr'):
                nazev_strany_elem = strana.find('td', headers='t1sa1 t1sb2')
                hlasy_strany_elem = strana.find('td', headers='t1sa2 t1sb3')
                if nazev_strany_elem and hlasy_strany_elem:
                    nazev_strany = nazev_strany_elem.text.strip()
                    hlasy_strany = hlasy_strany_elem.text.strip()
                    strany_hlasy[nazev_strany] = hlasy_strany
                    all_strany.add(nazev_strany)

            # Zapis dat do seznamu
            row = [kod_obce, nazev_obce, volici_v_seznamu, vydane_obalky, platne_hlasy]
            for nazev_strany in all_strany:
                row.append(strany_hlasy.get(nazev_strany, '0'))
            rows.append(row)

# Open CSV soubor pro zápis
print(f"UKLADAM DO SOUBORU: {args.output_file}")
with open(args.output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
    header.extend(all_strany)
    writer.writerow(header)

    # Zapis dat do CSV souboru
    for row in rows:
        writer.writerow(row)

print("UKONCUJI: projekt_3.py")
