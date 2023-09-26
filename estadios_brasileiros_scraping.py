# importando pacotes importantes
from bs4 import BeautifulSoup
import pandas as pd

# selenium 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from time import sleep

service = Service()
options = webdriver.ChromeOptions()
options.add_argument('--headless')               # executar o código sem manter a página aberta
# options.add_argument('window-size=400,800')    # escolhendo o tamanho em que a página vai abrir
options.add_experimental_option("detach", True)  # impedi a página de fechar automaticamente após abrir

navegador = webdriver.Chrome(options=options, service=service) # instanciando o webdriver com alguns 'options' setados
navegador.get('https://pt.wikipedia.org/wiki/Lista_dos_maiores_est%C3%A1dios_de_futebol_do_Brasil')

sleep(5)

# a tabela em questao continha células que abrangiam mais de uma linha, dificultando a raspagem com o pacote requests
# procurando o elemento 'span'
position_span = navegador.find_element(By.XPATH,
                                       "//*[contains(concat( ' ', @class, ' ' ), concat( ' ', 'headerSort', ' ' ))]")
navegador.implicitly_wait(2)
position_span.click()                                      # clicando no span para reordenar a tabela assim realinhando as linhas corretamente

site = BeautifulSoup(navegador.page_source, 'html.parser') # passando o html para o beautifulsoup 

table = site.find("table", {"class": "wikitable"})         # procurando a tabela desejada e salvando na variavel 'table'    

# selecionando os headers das colunas
headers = [header.text.strip() for header in table.find_all('th')]
headers = headers[1:6]

rows = [] #cria uma lista vazia
for row in table.find_all('tr')[1:]: 
    value = row.find_all('td')                             # salva os valores da linha atual

    beautified_value = [ele.text.strip() for ele in value] # salva cada elemento individualmente da linha atual em uma lista

    if len(beautified_value) == 0:                         # remove os data arrays que estão vazios
        continue
    
    rows.append(beautified_value)                          # faz o append da linha na lista 'rows'

df = pd.DataFrame(rows, columns=headers)                   # salva em um dataframe
df.to_csv('brazilian-stadiums.csv', index=False)           # salva em um arquivo csv
