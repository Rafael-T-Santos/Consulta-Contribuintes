import pandas as pd
import numpy as np
import os
import time
import tempfile
import shutil
import sys
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

hoje = datetime.today().strftime('%Y-%m-%d')
ontem = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')

sexto_arquivo = (datetime.today() - timedelta(5)).strftime('%Y-%m-%d')

service = Service(executable_path=ChromeDriverManager().install())

download_temp = tempfile.mkdtemp()
destino = r"E:\Destino 2"
prefs = {
'download.default_directory': download_temp,
'download.prompt_for_download': False,
'safebrowsing.enabled': True,
}

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')

driver = webdriver.Chrome(service = service, options = options)
driver.implicitly_wait(1)

def download_planilha():
    exit = 0
    diretorio = os.listdir(download_temp)
    qt_arquivos = len(diretorio)

    driver.get("http://nfe.sefaz.ba.gov.br/servicos/nfenc/Modulos/Geral/NFENC_consulta_cadastro_ccc.aspx")
    print('Acessando site.')

    select = Select(driver.find_element(By.NAME, 'CmdUF'))
    select.select_by_value('AL')

    filtro = driver.find_element(By.NAME, 'AplicarFiltro')
    filtro.click()
    print('Selecionada UF = AL, aguardando conclusão do filtro.')
    time.sleep(30)

    #total = driver.find_element(By.ID, 'lblTotal')
    try:
        driver.find_element(By.ID, 'lblTotal')
        time.sleep(15)
        driver.find_element(By.ID, 'lblTotal')
    except:
        driver.find_element(By.ID, 'PHConteudo_desTipoErro')
        print('Ops! Algo deu errado.')
        exit = 1
        arquivo = open(f"{destino}\\log.txt", "a")
        arquivo.write(f"Sefaz retornou mensagem de erro em - {datetime.today()}\n")

    if exit == 1:
        sys.exit('O Sistema encontrou um erro e será fechado.')
    else:
        pass

    planilha = driver.find_element(By.NAME, 'btn_GerarPlanilha')
    planilha.click()
    time.sleep(10)
    print('Gerando Planilha.')

    if qt_arquivos == len(os.listdir(download_temp)):
        time.sleep(10)
        try:
            driver.find_element(By.ID, 'PHConteudo_desTipoErro')
            print('Ops! Algo deu errado.')
            exit = 1
            arquivo = open(f"{destino}\\log.txt", "a")
            arquivo.write(f"Sefaz retornou mensagem de erro em - {datetime.today()}\n")
        except:
            pass
        
    else:
        print('Download em andamento.')
        time.sleep(30)

    if exit == 1:
        sys.exit('O Sistema encontrou um erro e será fechado.')
    else:
        pass

    files = os.listdir(download_temp)

    print('Movendo os arquivos e excluindo arquivos antigos.')
    for file in files:
        shutil.move(f"{download_temp}\\{file}", f"{destino}\\{hoje}-{file}")

    for file in os.listdir(destino):
        if sexto_arquivo in file:
            os.remove(f"{destino}\\{file}")
        else:
            pass
      
    print(f'Download efetuado com sucesso, os arquivos foram movidos para a pasta - {destino}')

    for file in os.listdir(destino):
        if ontem in file and 'rpt' in file:
            df1 = pd.read_csv(f'{destino}\\{file}', sep = ';')
        elif hoje in file and 'rpt' in file:
            df2 = pd.read_csv(f'{destino}\\{file}', sep = ';')
        else:
            pass
    
    print('Criando Dataframes e comparando arquivos de ontem e hoje.')

    df3 = df1.merge(df2, indicator=True, how = 'outer').loc[lambda v: v['_merge'] == 'right_only']
    df3.drop(columns=['Unnamed: 5', '_merge'], inplace = True)
    df3.to_csv(f"{destino}\\Alterações-{hoje}.csv", sep = ';', index = False)

    print(f'Criado novo arquivo apenas com as empresas que sofreram alteração.\nO arquivo foi salvo em - {destino}\\Alterações-{hoje}')
    arquivo = open(f"{destino}\\log.txt", "a")
    arquivo.write(f"Processo concluido com sucesso em - {datetime.today()}\n")
    
    driver.quit()

download_planilha()