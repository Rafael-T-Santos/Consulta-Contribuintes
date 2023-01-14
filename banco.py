import cryptocode
import csv
import pandas as pd
import pyodbc
import warnings
from datetime import datetime

warnings.filterwarnings("ignore", category=UserWarning)

chave = 'canetaazul'

def descriptografar(mensagem, chave):
    MensagemDescriptografada = cryptocode.decrypt(mensagem, chave)
    return(MensagemDescriptografada)

df = pd.read_csv('_config\config.csv', delimiter=';')

df['server'][0] = descriptografar(df['server'][0], chave)
df['database'][0] = descriptografar(df['database'][0], chave)
df['username'][0] = descriptografar(df['username'][0], chave)
df['password'][0] = descriptografar(df['password'][0], chave)

server = df['server'][0]
database = df['database'][0]
username = df['username'][0]
password = df['password'][0]

def testar_conexao(df2):
    print(df2)
    if df2['sistema'][0] == 'Questor':
        try:
            pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
            return True
        except:
            return False
    elif df2['sistema'][0] == 'Winthor':
        print('Winthor')
        return False
    else:
        print('Ocorreu algum erro!')
        return False
    
def consulta_clientes_questor():
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    df_sql = pd.DataFrame()

    consulta = f"""SELECT
                    T1.NR_CPFCNPJ AS 'CNPJ do Contribuinte', 
                    REPLACE(REPLACE(T1.NR_IE, '.', ''), '-', '') AS 'Inscricao Estadual',
                    T1.DS_ENTIDADE AS 'Razao Social',
                    T2.DS_UF AS 'UF',
                    CASE WHEN T1.X_ATIVO = 1 THEN 'Ativo' ELSE 'Inativo' END AS Situacao 
                        FROM TBL_ENTIDADES T1
                            INNER JOIN TBL_ENDERECO_CIDADES T2
                                ON T1.CD_CIDADE = T2.CD_CIDADE
                                WHERE T1.X_CLIENTE = 1;
                """
    df_sql = pd.read_sql_query(consulta, cnxn)
    return df_sql

def consulta_clientes_winthor():
    

    consulta = f"""SELECT 
                    CGCENT AS "CNPJ do Contribuinte",
                    IEENT AS "Inscricao Estadual",
                    CLIENTE AS "Razao Social",
                    ESTENT AS "UF"
                        FROM PCCLIENT
                            WHERE ESTENT = 'AL';                    
                """

"""df2 = df
df2['sistema'] = 'Questor'
print(testar_conexao(df2))"""