import time
from BotDownloadCertificado import BotDownloadCertificado

tempo_ini = time.time()

nome_buscar = input("Digite seu nome completo: ")

obj_bot = BotDownloadCertificado(nome_buscar=nome_buscar)
obj_bot.exec_bot()

print("Tempo gasto com execução: ", time.time() - tempo_ini)
