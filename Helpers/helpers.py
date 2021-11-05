import os
import json
import time
import platform
from time import sleep
from threading import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def cria_driver(caminho_pasta_download_pdfs):
    chrome_options = webdriver.ChromeOptions()
    settings = {"recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
                "selectedDestinationId": "Save as PDF", "version": 2
                }

    prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings),
                "download.default_directory": caminho_pasta_download_pdfs,
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": False,
                "safebrowsing_for_trusted_sources_enabled": False,
                'download.extensions_to_open': 'msg',
                "plugins.always_open_pdf_externally": True}

    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')

    navegador = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver/chromedriver', chrome_options=chrome_options)
    return navegador


def espera_um_elemento_por_xpath(navegador, xpath, tempo):
    wait = WebDriverWait(navegador, tempo)
    wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    return navegador.find_element_by_xpath(xpath)


def espera_um_elemento_por_id(navegador, id, tempo):
    wait = WebDriverWait(navegador, tempo)
    wait.until(EC.visibility_of_element_located((By.ID, id)))
    return navegador.find_element_by_id(id)


def espera_um_elemento_por_classe(navegador, classe, tempo):
    wait = WebDriverWait(navegador, tempo)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, classe)))
    return navegador.find_element_by_class_name(classe)


def espera_um_elemento_por_nome(navegador, nome, tempo):
    wait = WebDriverWait(navegador, tempo)
    wait.until(EC.visibility_of_element_located((By.NAME, nome)))
    return navegador.find_element_by_name(nome)