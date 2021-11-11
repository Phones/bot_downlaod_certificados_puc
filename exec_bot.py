import os
import time
import platform
from threading import Thread
from BotDownloadCertificado import BotDownloadCertificado

tempo_ini = time.time()

sistema = ''
def get_padrao_barra():
    # Verifica qual sistema está sendo utilizado pelo usuario
    sistema = platform.system()

    padrao_barra = '/'
    if sistema == 'Windows':
        padrao_barra = "\\"

    return padrao_barra

def verifica_e_cria_pasta_pdfs(padrao_barra, nome_buscar):
    caminho =  os.getcwd() + padrao_barra + nome_buscar.replace(' ', '_') + '_PDFs'
    if not os.path.exists(caminho):
        os.makedirs(caminho)

    # Cria o arquivo que armazena o nome dos eventos que encontrou
    arq = open(caminho + padrao_barra + 'eventos_que_nome_existe.txt', 'w')
    arq.write('Eventos que encontrou certificado:\n')
    arq.close()

    return caminho


def get_quantidade_eventos(padrao_barra):
    # Apenas acessa a pagina e busca a quantidade de eventos
    obj_bot = BotDownloadCertificado(nome_buscar=nome_buscar, ini=0, fim=0, padrao_barra=padrao_barra, caminho_para_pasta_download='')
    obj_bot.navegador.get(obj_bot.url)
    quant = obj_bot.coleta_quantidade_de_eventos()
    obj_bot.navegador.close()
    
    return quant

def monta_lista_threads(quantidade_threads, nome_buscar, padrao_barra, caminho_para_pasta_download):
    lista_threads = []
    quant_eventos = get_quantidade_eventos(padrao_barra)
    div = int(quant_eventos / quantidade_threads)
    resto = quant_eventos % quantidade_threads

    ini, fim = 1, div
    for i in range(quantidade_threads):
        print("Inicio: {} / Fim: {}".format(ini, fim))
        obj_bot = BotDownloadCertificado(nome_buscar=nome_buscar, ini=ini, fim=fim, padrao_barra=padrao_barra, caminho_para_pasta_download=caminho_para_pasta_download)
        lista_threads.append(Thread(target=obj_bot.exec_bot))
        ini += div
        fim += div

    if resto != 0:
        ini, fim = (quant_eventos - resto), (quant_eventos + 1)
        print("Inicio: {} / Fim: {}".format(ini, fim))
        obj_bot = BotDownloadCertificado(nome_buscar=nome_buscar, ini=ini, fim=fim, padrao_barra=padrao_barra, caminho_para_pasta_download=caminho_para_pasta_download)
        lista_threads.append(Thread(target=obj_bot.exec_bot))

    return lista_threads

def exec_threads(lista_treads):

    print("Stardando todas as Threads!")
    # Estarta todas as threads
    for _thread_ in lista_treads:
        _thread_.start()

    # Espera todas as threads finalizar
    for _thread_ in lista_treads:
        _thread_.join()



nome_buscar = input("Digite seu nome completo: ")
nome_buscar = nome_buscar.upper()
quantidade_threads = 2
'''
print("-------------------------------------------------------------------------------")
print("Por padrão, o bot utilizada apenas 2 threads, porém essa valor é alteravel!")
resp = input("              Deseja alterar o número de threads? (s/n):      ")
if resp.upper() == "S":
    quantidade_threads = int(input("Insira o novo número de threads: "))
    print("Valor alterado com sucesso!")
print("-------------------------------------------------------------------------------")
'''
padrao_barra=get_padrao_barra()
caminho_para_pasta_download = verifica_e_cria_pasta_pdfs(padrao_barra=padrao_barra, nome_buscar=nome_buscar)
exec_threads(monta_lista_threads(quantidade_threads=quantidade_threads, nome_buscar=nome_buscar, padrao_barra=padrao_barra, caminho_para_pasta_download=caminho_para_pasta_download))
print("Tempo gasto com execução: ", time.time() - tempo_ini)
