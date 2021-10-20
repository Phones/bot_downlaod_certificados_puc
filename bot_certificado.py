from Helpers.helpers import *

tempo_ini = time.time()

def verifica_e_cria_pasta_pdfs(nome_buscar):
    caminho =  os.getcwd() + '/' + nome_buscar.replace(' ', '_') + '_PDFs'
    if not os.path.exists(caminho):
        os.makedirs(caminho)

    return caminho

nome_buscar = input("Digite seu nome completo: ")
nome_buscar = nome_buscar.upper()
caminho_pasta_pdfs = verifica_e_cria_pasta_pdfs(nome_buscar)

navegador = cria_driver(caminho_pasta_pdfs)
navegador.get("https://sites.pucgoias.edu.br/certificados/")

# Coleta a quantidade de eventos que existem
xpath = '/html/body/div/div[1]/div/table/tbody/tr'
espera_um_elemento_por_xpath(navegador, xpath, 10)
quant_eventos = len(navegador.find_elements_by_xpath(xpath)) + 1

nomes_eventos_nome_existe = ''
for i in range(1, quant_eventos):
    print("num: ", i)
    # Clica no evento
    xpath_evento = '/html/body/div/div[1]/div/table/tbody/tr[' + str(i) + ']/td/a'
    elemento_evento = espera_um_elemento_por_xpath(navegador=navegador, xpath=xpath_evento, tempo=5)
    nome_evento = elemento_evento.text
    elemento_evento.click()

    # Coleta a lista de nomes do evento
    xpath_lista_nomes = '/html/body/div/div[1]'
    nomes = espera_um_elemento_por_xpath(navegador=navegador, xpath=xpath_lista_nomes, tempo=5).text

    nomes = nomes.upper()
    if nome_buscar in nomes:
        print("ENCONTROU! NOME DO EVENTO: ", nome_evento)
        nomes_eventos_nome_existe += nome_evento.replace('\n', '') + '\n'

        # Faz download do certificado
        lista_nomes = nomes.split('\n')
        xpath_do_pdf = '/html/body/div/div[1]/div/table/tbody/tr[' + str(lista_nomes.index(nome_buscar)) + ']/td/a'
        espera_um_elemento_por_xpath(navegador=navegador, xpath=xpath_do_pdf, tempo=5).click()
    
    navegador.back()

arq = open(caminho_pasta_pdfs + '/eventos_que_nome_existe.txt', 'w')
arq.write(nomes_eventos_nome_existe)
arq.close()

print("Tempo gasto com execução: ", time.time() - tempo_ini)
