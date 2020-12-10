import os
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait

from helpers import print_timestamp


class Mei:
    def __init__(self, driver, files_path, uf):
        self.driver = driver
        self.files_path = os.path.join(os.getcwd(), files_path)
        # print(self.files_path)
        self.uf = uf

    def _retorna_xpath(self, driver, timeout, freq, xpath):
        wbw = WebDriverWait(driver=driver,
                            timeout=timeout,
                            poll_frequency=freq)
        wbw.until(presence_of_element_located((By.XPATH, xpath)),
                  "Elemento não encontrado.")
        xpath = driver.find_element_by_xpath(xpath)
        return xpath

    def retorna_tabela(self, xpath_btn_consulta, xpath_tab_completa):
        time.sleep(2)
        print('Extraindo tabela.', print_timestamp())
        tentativas = [1, 2, 3]
        for i in tentativas:
            print(f"Tentativa {i} de 3...")
            self.driver.find_element_by_xpath(xpath_btn_consulta).click()
            try:
                self._retorna_xpath(self.driver, 150, 5, xpath_tab_completa)
                print('Tabela carregada.', print_timestamp())
                return True
            except TimeoutException:
                print('Tabela não foi carregada.')
        return False

    def del_arquivos_inuteis(self):
        files_path = self.files_path
        for file in os.listdir(files_path):
            if file[:13] == 'relatorio_mei':
                os.remove(os.path.join(files_path, file))

    def renomeia_arquivo(self):
        files_path = self.files_path
        uf = self.uf
        file = r'relatorio_mei.csv'
        if file in os.listdir(files_path):
            old_file = os.path.join(files_path, file)
            new_file = r'{}_cnae_e_municipios_{}.csv'.format(
                uf, print_timestamp(now=False)
            )
            new_file = os.path.join(files_path, new_file)
            try:
                os.rename(old_file, new_file)
                print(f"Arquivo renomeado para {new_file} " + print_timestamp())
            except FileExistsError:
                print("Arquivo já existe.")

    def verifica_arquivo(self):
        files_path = self.files_path
        if not os.path.exists(files_path):
            os.mkdir(files_path)
            print(f"Arquivos baixados ficarão na pasta {files_path}.")
        uf = self.uf
        data = print_timestamp(now=False)
        name = f"{uf}_cnae_e_municipios_{data}.csv"
        if name in os.listdir(files_path):
            return name
        else:
            return False

    def exporta_csv(self):
        driver = self.driver
        xpath_btn_exportar = '//*[@id="form:botaoExportarCsv"]'
        driver.find_element_by_xpath(xpath_btn_exportar).click()
        time.sleep(10)
        print('Download concluído.', print_timestamp())

    def abre_browser(self):
        url = 'http://www22.receita.fazenda.gov.br/inscricaomei/private/pages/relatorios/opcoesRelatorio.jsf#'
        xpath = '/html/body/table/tbody/tr[2]/td/form/div/div/div[1]/p'

        while True:
            driver = self.driver
            try:
                driver.get(url)
                print('Browser iniciado. ' + print_timestamp())
                self._retorna_xpath(driver, 15, 5, xpath)
                break
            except TimeoutException as e:
                driver.quit()
                print(e)

    def carrega_pagina_relatorio(self, xpath_page):
        driver = self.driver
        page = driver.find_element_by_xpath(xpath_page)
        page.click()

    def uf_listbox(self, xpath_listbox):
        time.sleep(5)
        driver = self.driver
        uf = self.uf
        el = driver.find_element_by_xpath(xpath_listbox)
        for option in el.find_elements_by_tag_name('option'):
            if option.text == uf:
                option.click()
                break


class MeiCnaeMunicipio(Mei):
    xpath_page = '/html/body/table/tbody/tr[2]/td/form/div/div/div[1]/ul/li[6]/a'
    xpath_listbox = '//*[@id="form:uf"]'
    xpath_municipios = '//*[@id="form:listaMunicipiosUF"]'
    xpath_relatorio = '//*[@id="form:listaMunicipiosRelatorio"]'
    xpath_btn_inserir = '//*[@id="form:btnInserir"]'
    xpath_btn_consulta = '//*[@id="form:botaoConsultar"]'
    xpath_tab_completa = '//*[@id="form:j_id62"]'

    def __init__(self, driver, files_path, uf):
        super().__init__(driver, files_path, uf)

    def verifica_listbox_municipios(self):
        driver = self.driver
        for tries in [1, 2, 3]:
            print(f"Carregando municípios. Tentativa {tries}/3.", print_timestamp())
            time.sleep(5)
            # verifica se a 1a listbox está preenchida
            cities = driver.find_element_by_xpath(self.xpath_municipios)
            n_cities = len(cities.text.split('\n'))
            if n_cities > 1 or cities.text == 'BRASILIA':
                cities.find_elements_by_tag_name('option')[0].click()
                cities.send_keys(Keys.SHIFT, Keys.END)
                driver.find_element_by_xpath(self.xpath_btn_inserir).click()
                time.sleep(5)
                # verifica se a 2a listbox está preenchida
                rel = driver.find_element_by_xpath(self.xpath_relatorio)
                n_rel = len(rel.text.split('\n'))
                if n_rel > 1 or rel.text == 'BRASILIA':
                    print("Municipíos carregados.")
                    break
            # se nao atenderem as condições
            if n_cities <= 1 and tries == 3:
                print("Não foi possível carregar os municípios.")
                return False
        return True
