# Consulta-Contribuintes
Script para efetuar download de csv contendo informações de situação cadastral dos contribuintes de Alagoas

Ao executar o script main.py o sistema abre o google chrome em segundo plano, acessa o site da sefaz da Bahia e faz a pesquisa por contribuintes de Alagoas, ao concluir a pesquisa é feita requisição de download dessa planilha, a mesma é salva em uma pasta de destino junto com a data o qual foi baixada, ao executar o script no dia posterior o script faz os mesmos procedimentos e dessa vez compara os dois arquivos, do dia anterior com o dia atual e gera um novo arquivo mostrando apenas as diferenças entre eles, fazendo com que se tenha bem menos dados para se trabalhar.

Site utilizado - http://nfe.sefaz.ba.gov.br/servicos/nfenc/Modulos/Geral/NFENC_consulta_cadastro_ccc.aspx
