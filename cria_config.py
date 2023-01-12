import cryptocode
import pandas as pd
import flet
from flet import (  Page, ElevatedButton, Text, TextField,
                    AlertDialog, TextButton, MainAxisAlignment)

chave = 'asjkfa&_jsa&%jasfka*'

def criptografar(mensagem, chave):
    MensagemCriptografada = cryptocode.encrypt(mensagem, chave)
    return(MensagemCriptografada)

def descriptografar(mensagem, chave):
    MensagemDescriptografada = cryptocode.decrypt(mensagem, chave)
    return(MensagemDescriptografada)

def main(page: Page):
    page.title = 'Criar arquivo de conexão'
    page.theme_mode = 'light'
    page.window_width = 500
    page.window_min_width = 500
    page.window_height = 500
    page.window_min_height = 500
    page.horizontal_alignment = 'center'
    page.padding = 10
    page.update()

    global txt_server, txt_database, txt_username, txt_password

    def cripto_arquivo(e):
        df = {'server': [txt_server.value],
            'database': [txt_database.value],
            'username': [txt_username.value],
            'password': [txt_password.value]
        }

        df = pd.DataFrame(data=df)

        df['server'][0] = criptografar(df['server'][0], chave)
        df['database'][0] = criptografar(df['database'][0], chave)
        df['username'][0] = criptografar(df['username'][0], chave)
        df['password'][0] = criptografar(df['password'][0], chave)

        df.to_csv('_config\config.csv', index=False, sep=';')
        close_dlg(e)

    def descripto_arquivo(e):
        df = pd.read_csv('_config\config.csv', delimiter=';')

        df['server'][0] = descriptografar(df['server'][0], chave)
        df['database'][0] = descriptografar(df['database'][0], chave)
        df['username'][0] = descriptografar(df['username'][0], chave)
        df['password'][0] = descriptografar(df['password'][0], chave)

        df.to_csv('_config\config.csv', index=False, sep=';')
        close_dlg(e)

    def open_dlg_modal(e):
        if txt_server.value == 'cimacimabaixobaixoesquerdadireitaesquerdadireitabastart':
            page.dialog = konamicode
            konamicode.open = True
            btn_decr.visible = True
            page.update()
        else:
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()
    
    def close_dlg(e):
        dlg_modal.open = False
        page.update()
    
    def close_konami(e):
        konamicode.open = False
        page.update()

    txt_server = TextField(label="servidor,porta", hint_text='Insira o IP e porta do servidor', width=390, helper_text='Exemplo: 192.168.0.1,8888')
    txt_database = TextField(label="database", hint_text='Insira o nome do banco', width=390)
    txt_username = TextField(label="username", hint_text='Insira o usuário do banco', width=390)
    txt_password = TextField(label="password", hint_text='Insira a senha do usuário', width=390)
    btn_criar = ElevatedButton('Criar Arquivo', on_click=open_dlg_modal, width=200)
    btn_decr = ElevatedButton('Descriptografar', on_click=descripto_arquivo, width=200, visible=False, icon="videogame_asset")

    dlg_modal = AlertDialog(
        modal=True,
        title=Text("Confirmar"),
        content=Text("Confirma as informações digitadas?"),
        actions=[
            TextButton("Sim", on_click=cripto_arquivo),
            TextButton("Não", on_click=close_dlg)
        ],
        actions_alignment=MainAxisAlignment.CENTER
    )

    konamicode = AlertDialog(
        modal=True,
        title=Text("Parabéns!"),
        content=Text("Você desbloqueou a função Descriptografar."),
        actions=[
            TextButton("OK", on_click=close_konami)
        ],
        actions_alignment=MainAxisAlignment.CENTER
    )

    page.add(txt_server,txt_database,txt_username,txt_password, btn_criar, btn_decr)


flet.app(name='Criar arquivo de conexão', target=main)