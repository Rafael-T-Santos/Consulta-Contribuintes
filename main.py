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

import banco as b
import cryptocode

chave = 'canetaazul'

def descriptografar(mensagem, chave):
    MensagemDescriptografada = cryptocode.decrypt(mensagem, chave)
    return(MensagemDescriptografada)

df = pd.read_csv('_config\config.csv', delimiter=';')

sistema = descriptografar(df['sistema'][0], chave)

hoje = datetime.today().strftime('%Y-%m-%d')
ontem = (datetime.today() - timedelta(1)).strftime('%Y-%m-%d')

sexto_arquivo = (datetime.today() - timedelta(5)).strftime('%Y-%m-%d')

service = Service(executable_path=ChromeDriverManager().install())

download_temp = tempfile.mkdtemp()
destino = "Destino"
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
driver.implicitly_wait(5)

def download_planilha():
    exit = 0
    diretorio = os.listdir(download_temp)
    qt_arquivos = len(diretorio)

    driver.get("http://nfe.sefaz.ba.gov.br/servicos/nfenc/Modulos/Geral/NFENC_consulta_cadastro_ccc.aspx")
    print('Acessando site.')

    select = Select(driver.find_element(By.NAME, 'CmdUF'))
    #uf = input('Digite a sigla da UF que deseja efetuar o download.')
    #uf = uf.upper()
    uf = 'AL'
    select.select_by_value(uf)

    filtro = driver.find_element(By.NAME, 'AplicarFiltro')
    filtro.click()
    print(f'Selecionada UF = {uf}, aguardando conclusão do filtro.')
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
    try:
        for file in files:
            shutil.move(f"{download_temp}\\{file}", f"{destino}\\Downloads\\{hoje}-{file}")
    except:
        time.sleep(30)
        for file in files:
            shutil.move(f"{download_temp}\\{file}", f"{destino}\\Downloads\\{hoje}-{file}")

    for file in os.listdir("Destino\\Downloads"):
        if sexto_arquivo in file:
            os.remove(f"{destino}\\Downloads\\{file}")
        else:
            pass

    print(f'Download efetuado com sucesso, os arquivos foram movidos para a pasta - {destino}\Downloads')

    for file in os.listdir("Destino\\Downloads"):
        if ontem in file and 'rpt' in file:
            try:
                df1 = pd.read_csv(f'{destino}\\Downloads\\{file}', sep = ';')
            except:
                arquivo = open(f"{destino}\\log.txt", "a")
                arquivo.write(f"Não existe arquivo de ontem para comparar, volte amanhã. - {datetime.today()}\n")
        elif hoje in file and 'rpt' in file:
            try:
                df2 = pd.read_csv(f'{destino}\\Downloads\\{file}', sep = ';')
            except:
                arquivo = open(f"{destino}\\log.txt", "a")
                arquivo.write(f"Ocorreu algum problema, contate o suporte. - {datetime.today()}\n")
        else:
            pass
    
    print('Criando Dataframes e comparando arquivos de ontem e hoje.')

    try:
        df3 = df1.merge(df2, indicator=True, how = 'outer').loc[lambda v: v['_merge'] == 'right_only']
        df3.drop(columns=['Unnamed: 5', '_merge'], inplace = True)
        df3.to_csv(f"{destino}\\Alteracoes\\Alterações-{hoje}.csv", sep = ';', index = False)
        df3 = df3.astype(str)
    except:
        pass

    try:
        if sistema == 'Questor':
            df4 = b.consulta_clientes_questor()
        elif sistema == 'Winthor':
            df4 = b.consulta_clientes_winthor()

        df5 = df4.merge(df3, indicator=True, how = 'inner', on = ['CNPJ do Contribuinte', 'Inscricao Estadual'])
        df5.drop(columns=['Razao Social_y','UF_y', '_merge'], inplace = True)
        df5.rename(columns={'Razao Social_x': 'Razao Social',
                            'UF_x': 'UF',
                            'Situacao_x': 'Situacao Cadastro',
                            'Situacao_y': 'Situacao SEFAZ'}, inplace = True)
        df5.to_csv(f"{destino}\\Clientes\\{sistema}-{hoje}.csv", sep = ';', index = False)

        print(f'Criado novo arquivo apenas com as empresas que sofreram alteração.\nO arquivo foi salvo em - {destino}\\Clientes\\{sistema}-{hoje}')
        arquivo = open(f"{destino}\\log.txt", "a")
        arquivo.write(f"Processo concluido com sucesso em - {datetime.today()}\n")
    except:
        arquivo = open(f"{destino}\\log.txt", "a")
        arquivo.write(f"Ocorreu algum problema de conexão com o banco de dados, contate o suporte. - {datetime.today()}\n")
    
    driver.quit()

download_planilha()