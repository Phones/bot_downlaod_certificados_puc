from threading import Thread
import time
from BotDownloadCertificado import BotDownloadCertificado

tempo_ini = time.time()

def get_quantidade_eventos():
    # Apenas acessa a pagina e busca a quantidade de eventos
    obj_bot = BotDownloadCertificado(nome_buscar=nome_buscar, ini=0, fim=0)
    obj_bot.navegador.get(obj_bot.url)
    quant = obj_bot.coleta_quantidade_de_eventos()
    obj_bot.navegador.close()
    
    return quant

def monta_lista_threads(quantidade_threads, nome_buscar):
    lista_threads = []
    quant_eventos = get_quantidade_eventos()
    div = int(quant_eventos / quantidade_threads)
    resto = quant_eventos % quantidade_threads
    
    print(resto)
    ini, fim = 1, div
    for i in range(quantidade_threads):
        print("Inicio: {} / Fim: {}".format(ini, fim))
        obj_bot = BotDownloadCertificado(nome_buscar=nome_buscar, ini=ini, fim=fim)
        lista_threads.append(Thread(target=obj_bot.exec_bot))
        ini += div
        fim += div

    if resto != 0:
        ini, fim = (quant_eventos - resto), (quant_eventos + 1)
        print("Inicio: {} / Fim: {}".format(ini, fim))
        obj_bot = BotDownloadCertificado(nome_buscar=nome_buscar, ini=ini, fim=fim)
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
quantidade_threads = 2

print("-------------------------------------------------------------------------------")
print("Por padrão, o bot utilizada apenas 2 threads, porém essa valor é alteravel!")
resp = input("              Deseja alterar o número de threads? (s/n):      ")
if resp.upper() == "S":
    quantidade_threads = int(input("Insira o novo número de threads: "))
    print("Valor alterado com sucesso!")
print("-------------------------------------------------------------------------------")

exec_threads(monta_lista_threads(quantidade_threads=quantidade_threads, nome_buscar=nome_buscar))
print("Tempo gasto com execução: ", time.time() - tempo_ini)
