import cryptocode
import pandas as pd
import flet
from flet import (  Page, ElevatedButton, Text, TextField,
                    AlertDialog, TextButton, MainAxisAlignment,
                    Dropdown, dropdown, Row)

import banco as b

chave = 'canetaazul'

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
    page.window_center()
    page.update()

    global txt_server, txt_database, txt_username, txt_password

    def testar_conexao(e):
        conexao = False
        if txt_server.value == '' or txt_database.value == '' or txt_username.value == '' or txt_password.value == '' or drop_sistema.value == None:
            page.dialog = erro_modal
            erro_modal.open = True
            page.update()
        else:
            df = {'server': [txt_server.value],
                'database': [txt_database.value],
                'username': [txt_username.value],
                'password': [txt_password.value],
                'sistema': [drop_sistema.value]
            }
            conexao = b.testar_conexao(df)
            if conexao:
                page.dialog = teste_modal
                teste_modal.open = True
                page.update()
            else:
                page.dialog = teste_modal_erro
                teste_modal_erro.open = True
                page.update()

    def cripto_arquivo(e):
        df = {'server': [txt_server.value],
            'database': [txt_database.value],
            'username': [txt_username.value],
            'password': [txt_password.value],
            'sistema': [drop_sistema.value]
        }

        df = pd.DataFrame(data=df)

        df['server'][0] = criptografar(df['server'][0], chave)
        df['database'][0] = criptografar(df['database'][0], chave)
        df['username'][0] = criptografar(df['username'][0], chave)
        df['password'][0] = criptografar(df['password'][0], chave)
        df['sistema'][0] = criptografar(df['sistema'][0], chave)

        df.to_csv('_config\config.csv', index=False, sep=';')
        close_dlg(e)

    def descripto_arquivo(e):
        df = pd.read_csv('_config\config.csv', delimiter=';')

        df['server'][0] = descriptografar(df['server'][0], chave)
        df['database'][0] = descriptografar(df['database'][0], chave)
        df['username'][0] = descriptografar(df['username'][0], chave)
        df['password'][0] = descriptografar(df['password'][0], chave)
        df['sistema'][0] = criptografar(df['sistema'][0], chave)

        df.to_csv('_config\config.csv', index=False, sep=';')
        close_dlg(e)

    def open_dlg_modal(e):
        if txt_server.value == 'cimacimabaixobaixoesquerdadireitaesquerdadireitabastart':
            page.dialog = konamicode
            konamicode.open = True
            btn_decr.visible = True
            page.window_height = 550
            page.window_min_height = 550
            page.update()
        elif txt_server.value == '' or txt_database.value == '' or txt_username.value == '' or txt_password.value == '' or drop_sistema.value == None:
            page.dialog = erro_modal
            erro_modal.open = True
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

    def close_erro(e):
        erro_modal.open = False
        page.update()

    def close_teste(e):
        teste_modal.open = False
        page.update()
    
    def close_teste_erro(e):
        teste_modal_erro.open = False
        page.update()

    txt_server = TextField(label="servidor,porta", hint_text='Insira o IP e porta do servidor', width=390, helper_text='Exemplo: 192.168.0.1,8888 ou 192.168.0.1', prefix_icon="computer")
    txt_database = TextField(label="database", hint_text='Insira o nome do banco', width=390, prefix_icon="account_tree_outlined")
    txt_username = TextField(label="username", hint_text='Insira o usuário do banco', width=390, prefix_icon="account_box_outlined")
    txt_password = TextField(label="password", hint_text='Insira a senha do usuário', width=390, prefix_icon="password", password=True, can_reveal_password=True)
    btn_criar = ElevatedButton('Criar Arquivo', on_click=open_dlg_modal, width=190, icon="check")
    btn_decr = ElevatedButton('Descriptografar', on_click=descripto_arquivo, width=150, visible=False, icon="videogame_asset")
    btn_testar = ElevatedButton('Testar Conexão', on_click=testar_conexao, width=190, icon="connected_tv")
    drop_sistema = Dropdown(label='Sistema',
                            hint_text='Escolha o sistema.',
                            options=[
                                dropdown.Option('Questor'),
                                dropdown.Option('Winthor')
                            ], width=390)

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

    erro_modal = AlertDialog(
        modal=True,
        title=Text("Ooops!"),
        content=Text("Você deve digitar e escolher todos os campos antes de prosseguir."),
        actions=[
            TextButton("OK", on_click=close_erro)
        ],
        actions_alignment=MainAxisAlignment.CENTER
    )

    teste_modal = AlertDialog(
        modal=True,
        title=Text("Teste de Conexão"),
        content=Text("Conexão bem sucedida!"),
        actions=[
            TextButton("OK", on_click=close_teste)
        ],
        actions_alignment=MainAxisAlignment.CENTER
    )

    teste_modal_erro = AlertDialog(
        modal=True,
        title=Text("Teste de Conexão"),
        content=Text("Impossível conectar, verifique todos os campos digitados e tente novamente."),
        actions=[
            TextButton("OK", on_click=close_teste_erro)
        ],
        actions_alignment=MainAxisAlignment.CENTER
    )

    page.add(txt_server,txt_database,txt_username,txt_password,drop_sistema, Row([btn_criar,btn_testar], alignment='center'), btn_decr)


flet.app(name='Criar arquivo de conexão', target=main)