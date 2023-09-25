from bs4 import BeautifulSoup
import requests as re
import pandas as pd

wiki_page_request = re.get(
    'https://pt.wikipedia.org/wiki/Lista_dos_maiores_est%C3%A1dios_de_futebol_do_Brasil')
wiki_page_text = wiki_page_request.text

site = BeautifulSoup(wiki_page_text, 'html.parser')

table = site.find("table", {"class": "wikitable"})

headers = [header.text.strip() for header in table.find_all('th')]
headers = headers[1:6]

rows = []
for row in table.find_all('tr')[1:]:
    value = row.find_all('td')
    beautified_value = [ele.text.strip() for ele in value]

    if len(beautified_value) == 0:
        continue
    
    rows.append(beautified_value)

df = pd.DataFrame(rows, columns=headers)
print(df.head(15))