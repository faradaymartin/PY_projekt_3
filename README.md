# Projekt 3
Třetí projekt na Python Akademii od Engeta

# Popis projektu
Tento projekt slouží k extahování výsledků z parlamentních voleb v roce 2017 - okres Ostrava-město. 
Odkaz: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8106

# Instalace knihoven
Knihovny, které jsem využil v kódu, jsou uložené v souboru requirements.txt. Pro instalaci doporučuji nové virtuální prostředí a s nainstalovaným manažerem spusit následovně:

$ pip --version
$ pip install -r requirements.txt

# Spuštění projektu
Spuštění souboru projekt_3.py v rámci při. řádku požaduje poviné dva argumenty.

python projekt_3.py <odkaz územního celku> a <výsledný soubor>
Následně data se stáhnout do souboru s přípomnou CSV.

# Ukázka projektu
Výsledky hlasování pro okres Ostrava-město:

1. argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8106
2. argument: vysledky_voleb.csv

Spuštění programu:
python projekt_3.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8106" vysledky_voleb.csv

Průběh stahování:
STAHUJI DATA Z VYBRANÉHO URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=14&xnumnuts=8106
UKLADAM DO SOUBORU: vysledky_voleb.csv
UKONČUJI: projekt_3.py

Ukázka částečného výstupu:
Kód obce,Název obce,Voliči v seznamu,Vydané obálky,Platné hlasy,Strana zelených,STAROSTOVÉ A NEZÁVISLÍ,..
569119,Čavisov,419,318,316,4,16,0,..
506711,Dolní Lhota,1 202,904,899,9,31,1,..
