#!/usr/bin/env python
# coding: utf-8

# # Automação Web e Busca de Informações com Python

# #### Desafio: 
# Trabalhamos em uma importadora e o preço dos nossos produtos é vinculado a cotação de:
# - Dólar
# - Euro
# - Ouro
# Precisamos pegar na internet, de forma automática, a cotação desses 3 itens e saber quanto devemos cobrar pelos nossos produtos, considerando uma margem de contribuição que temos na nossa base de dados.
# Base de Dados: https://drive.google.com/drive/folders/1KmAdo593nD8J9QBaZxPOG1yxHZua4Rtv?usp=sharing
# Para isso, vamos criar uma automação web:
# - Usaremos o selenium
# - Importante: baixar o webdriver

# webdrivers: Chrome -> chromedriver / Firefox -> geckodriver


#Passo 1 e 2: acessar cotação na internet e armazenar a informação
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

navegador = webdriver.Chrome() # selenium está instalado no diretório do Python da máquina.
#         = webdriver.Chrome("chromedriver.exe") -> caso o selenium esteja instalado apenas no diretório do projeto.

# Pegar cotação dolar
navegador.get('https://www.google.com.br/')
navegador.find_element(By.XPATH,
                       '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('cotação dolar')
navegador.find_element(By.XPATH,
                       '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
dolar = float(navegador.find_element(By.XPATH,
                        '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')) #tornar a informação em valor númerico flutuante (float)
print(f'{dolar:.2f}', type(dolar))

# Pegar cotação euro
navegador.get('https://www.google.com.br/')
navegador.find_element(By.XPATH, 
                       '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys('cotação euro')
navegador.find_element(By.XPATH, 
                       '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(Keys.ENTER)
euro = float(navegador.find_element(By.XPATH, 
                        '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute('data-value')) #tornar a informação em valor númerico flutuante (float)
print(f'{euro:.2f}', type(euro))

# Pegar cotação do ouro
navegador.get('https://www.melhorcambio.com/ouro-hoje')
ouro = navegador.find_element(By.XPATH, 
                        '//*[@id="comercial"]').get_attribute('value')
ouro = float(ouro.replace(',','.')) #primeiro trocar o decimal e dps tornar a informação em valor númerico flutuante (float)
print(f'{ouro:.2f}', type(ouro))

navegador.quit() #fechar o navegador


# ### Agora vamos atualizar a nossa base de preços com as novas cotações

# - Importando a base de dados

#Passo 3:  importar banco de dados para a pasta de trabalho
import pandas as pd

df = pd.read_excel('Produtos.xlsx')

#Passo 4: atualizar banco de dados (coluna "Cotação")
df.loc[df['Moeda'] == 'Dólar', 'Cotação'] = dolar
df.loc[df['Moeda'] == 'Euro', 'Cotação'] = euro
df.loc[df['Moeda'] == 'Ouro', 'Cotação'] = ouro

display(df)


# - Atualizando os preços e o cálculo do Preço Final

#Passo 5: atualizar banco de dados (demais colunas)
#Coluna Preço de Compra
df['Preço de Compra'] = df['Preço Original']*df['Cotação']

#Coluna Preço de Venda
df['Preço de Venda'] = df['Preço de Compra']*df['Margem']

display(df)


# ### Agora vamos exportar a nova base de preços atualizada

df.to_excel('Novos Produtos.xlsx', index = False)
