import requests
from bs4 import BeautifulSoup
import csv
import argparse
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrapování dat z webu a ukládání do CSV souboru.')
    parser.add_argument('url', type=str, help='Odkaz na územní celek, který chcete scrapovat')
    parser.add_argument('output_file', type=str, help='Jméno výstupního souboru => vysledky_voleb.csv')
    return parser.parse_args()

def validate_arguments(args):
    if not args.url.startswith("https://www.volby.cz/"):
        print("CHYBA: Neplatný odkaz. Ujisti se, že odkaz začíná 'https://www.volby.cz/'.")
        sys.exit(1)
    if not args.output_file.endswith(".csv"):
        print("CHYBA: Neplatný název souboru. Ujistěte se, že název souboru končí '.csv'.")
        sys.exit(1)

def fetch_page_content(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')

def extract_obce_links(soup):
    return [link for link in soup.find_all('a', href=True) if link.text.strip().isdigit()]

def fetch_obec_data(link):
    obec_url = "https://www.volby.cz/pls/ps2017nss/" + link['href']
    obec_response = requests.get(obec_url)
    return BeautifulSoup(obec_response.content, 'html.parser')

def extract_obec_info(obec_soup, link):
    kod_obce = link.text.strip()
    nazev_obce = extract_nazev_obce(obec_soup)
    volici_v_seznamu = extract_text(obec_soup.find('td', headers='sa2'))
    vydane_obalky = extract_text(obec_soup.find('td', headers='sa3'))
    platne_hlasy = extract_text(obec_soup.find('td', headers='sa6'))
    strany_hlasy = extract_strany_hlasy(obec_soup)
    return kod_obce, nazev_obce, volici_v_seznamu, vydane_obalky, platne_hlasy, strany_hlasy

def extract_nazev_obce(obec_soup):
    for h3 in obec_soup.find_all('h3'):
        if "Obec:" in h3.text:
            return h3.text.replace("Obec:", "").strip()
    return "N/A"

def extract_text(element):
    return element.text.strip() if element else "N/A"

def extract_strany_hlasy(obec_soup):
    strany_hlasy = {}
    for strana in obec_soup.find_all('tr'):
        nazev_strany_elem = strana.find('td', headers='t1sa1 t1sb2')
        hlasy_strany_elem = strana.find('td', headers='t1sa2 t1sb3')
        if nazev_strany_elem and hlasy_strany_elem:
            nazev_strany = nazev_strany_elem.text.strip()
            hlasy_strany = hlasy_strany_elem.text.strip()
            strany_hlasy[nazev_strany] = hlasy_strany
    return strany_hlasy

def write_to_csv(output_file, all_strany, rows):
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        header = ['Kód obce', 'Název obce', 'Voliči v seznamu', 'Vydané obálky', 'Platné hlasy']
        header.extend(all_strany)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)

def main():
    args = parse_arguments()
    validate_arguments(args)
    print(f"STAHUJI DATA Z VYBRANÉHO URL: {args.url}")
    soup = fetch_page_content(args.url)
    obce_links = extract_obce_links(soup)
    all_strany = set()
    rows = []
    for link in obce_links:
        obec_soup = fetch_obec_data(link)
        kod_obce, nazev_obce, volici_v_seznamu, vydane_obalky, platne_hlasy, strany_hlasy = extract_obec_info(obec_soup, link)
        all_strany.update(strany_hlasy.keys())
        row = [kod_obce, nazev_obce, volici_v_seznamu, vydane_obalky, platne_hlasy]
        for nazev_strany in all_strany:
            row.append(strany_hlasy.get(nazev_strany, '0'))
        rows.append(row)
    print(f"UKLADAM DO SOUBORU: {args.output_file}")
    write_to_csv(args.output_file, all_strany, rows)
    print("UKONCUJI: projekt_3.py")

if __name__ == "__main__":
    main()
