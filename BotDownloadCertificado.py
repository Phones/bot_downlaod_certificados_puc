from Helpers.helpers import *


class BotDownloadCertificado:
    def __init__(self, nome_buscar, ini, fim, padrao_barra, caminho_para_pasta_download) -> None:
        # Inicio e Fim do range de busca da thread
        self.ini, self.fim = ini, fim

        # Nome que será buscado nos eventos
        self.nome_buscar = nome_buscar

        # Armazena nome dos eventos em que o bot encontrou o nome buscado
        self.nomes_eventos_nome_existe = ''

        # Xpath base para acessar os congressos
        self.xpath_base = '/html/body/div/div[1]/div/table/tbody/tr'

        # Link onde os eventos estão disponiveis
        self.url = "https://sites.pucgoias.edu.br/certificados/"

        # Essa barra é utilizada para montar os caminhos e varia de acordo com cada sistema
        self.padrao_barra = padrao_barra

        # Verifica se a pasta já existe, se não cria a pasta e retorna o caminho
        self.caminho_para_pasta_pdfs = caminho_para_pasta_download

        # Instancia o chromedriver
        self.navegador = cria_driver(self.caminho_para_pasta_pdfs)

        # Pega o número do evento que deu erro ao acessar
        self.lista_erros_evento = []


    def salva_nomes_eventos(self):
        """Salva o nome de todos os eventos onde encontrou o nome buscado"""
        arq = open(self.caminho_para_pasta_pdfs + self.padrao_barra + 'eventos_que_nome_existe.txt', 'r')
        conteudo_arquivo = arq.read()
        arq.close()

        arq = open(self.caminho_para_pasta_pdfs + self.padrao_barra + 'eventos_que_nome_existe.txt', 'w')
        arq.write(conteudo_arquivo + self.nomes_eventos_nome_existe)
        arq.close()

    def coleta_quantidade_de_eventos(self) -> int:
        # Espera a tabela com a lista de eventos aparecer no site
        espera_um_elemento_por_xpath(navegador=self.navegador, xpath=self.xpath_base, tempo=10)

        # Coleta a quantidade de eventos disponiveis
        return len(self.navegador.find_elements_by_xpath(self.xpath_base)) + 1

    def get_web_element_evento(self, numero_evento):
        xpath_evento = self.xpath_base + '[' + str(numero_evento) + ']/td/a'
        return espera_um_elemento_por_xpath(navegador=self.navegador, xpath=xpath_evento, tempo=30)

    def get_lista_nomes_do_evento(self):
        # Coleta a lista de nomes do evento
        xpath_lista_nomes = '/html/body/div/div[1]'
        return espera_um_elemento_por_xpath(navegador=self.navegador, xpath=xpath_lista_nomes, tempo=30).text.upper()

    def downlaod_vertificado(self, lista_de_nomes_do_evento):
        # Faz download do certificado
        lista_nomes = lista_de_nomes_do_evento.split('\n')
        xpath_do_pdf = '/html/body/div/div[1]/div/table/tbody/tr[' + str(lista_nomes.index(self.nome_buscar)) + ']/td/a'
        espera_um_elemento_por_xpath(navegador=self.navegador, xpath=xpath_do_pdf, tempo=30).click()

    def consulta_evento(self, numero_evento):
        print("Evento número: ", numero_evento)

        # WebElement do evento
        web_element_evento = self.get_web_element_evento(numero_evento=numero_evento)
        nome_evento = web_element_evento.text
        # Acessa o evento
        web_element_evento.click()

        lista_de_nomes_do_evento = self.get_lista_nomes_do_evento()
        if self.nome_buscar in lista_de_nomes_do_evento:
            print("ENCONTROU! NOME DO EVENTO: ", nome_evento)
            self.nomes_eventos_nome_existe += nome_evento.replace('\n', '') + '\n'

            self.downlaod_vertificado(lista_de_nomes_do_evento=lista_de_nomes_do_evento)

        self.navegador.back()

    def percorre_eventos(self):
        """Passa por todos os eventos disponiveis, verificando se o buscado está na lista de nomes dos eventos"""

        print("Inicio do range de busca: {} / Fim do range de busca: {}".format(self.ini, self.fim))
        for i in range(self.ini, self.fim):
            try:
                self.consulta_evento(numero_evento=i)
            except:
                self.lista_erros_evento.append(i)

    def percorre_eventos_com_erro(self):
        # Volta para a página principal
        self.navegador.get(self.url)

        for num_evento_erro in self.lista_erros_evento:
            self.consulta_evento(numero_evento=num_evento_erro)

    def exec_bot(self):
        # Acessa a pagina com todos os eventos
        self.navegador.get(self.url)

        print("Nome para busca: ", self.nome_buscar)
        # Passa por todas os eventos e baixa os certificados
        self.percorre_eventos()

        # Gera o arquivo com os nomes dos eventos em que encontrou o nome
        self.salva_nomes_eventos()

        self.percorre_eventos_com_erro()

        self.navegador.close()
