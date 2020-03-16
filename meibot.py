"""
a bot that scrap micro entrepreneurs subscriptions data from brazilian IRS
V: 0.0.0.0

"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException, NoSuchWindowException


class MeiBot:

    def __init__(self, headless=True):
        self.url = 'http://www22.receita.fazenda.gov.br/inscricaomei/private/pages/relatorios/opcoesRelatorio.jsf#'
        self.headless = headless
        self.dir = os.getcwd() + r'/files'

    def _verify_dir(self):
        try:
            os.mkdir(self.dir)
            print('Files folder created at {}. Downloaded files will be there.'.format(self.dir))
        except OSError:
            pass

    def _verify_uf(self, driver, uf):
        with open("lista de uf.txt", "r", encoding='latin-1') as f:
            data = f.read()
            ufs = data.split('\n')[:-1]
            if uf in ufs:
                return uf
            print('Nome da UF errada.\nUtilize um dos nomes abaixo:\n{}'.format(ufs))
            driver.close()

    def _browser(self):
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", self.dir)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv")
        fp.set_preference("dom.disable_deforeunload", True)

        options = webdriver.FirefoxOptions()
        if self.headless:
            options.add_argument('-headless')

        driver = webdriver.Firefox(fp, options=options)
        print('Browser started. ' + self._print_time())
        driver.get(self.url)
        time.sleep(5)
        print('Connected. ' + self._print_time())
        return driver

    def ufs_por_municipio_e_cnae(self):
        with open('lista de uf.txt', 'r', encoding='latin-1') as f:
            file = f.readlines()
        ufs = [uf[:-1] for uf in file]

        for uf in ufs:
            self.uf_por_municipio_e_cnae(uf)

    def uf_por_municipio_e_cnae(self, uf='PERNAMBUCO'):
        self._verify_dir()
        driver = self._browser()
        uf = self._verify_uf(driver, uf)
        print('Extraindo {} por municípios e CNAE.'.format(uf))

        try:

            # CNAE/MUNICIPIO - browser.find_element_by_link_text('CNAE/Município')
            page = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td/form/div/div/div[1]/ul/li[6]/a')
            page.click()
            time.sleep(5)

            # selecting UF at listbox
            el = driver.find_element_by_xpath('//*[@id="form:uf"]')
            for option in el.find_elements_by_tag_name('option'):
                if option.text == uf:
                    option.click()
                    break
            time.sleep(5)

            # selecting all the cities
            cities = driver.find_element_by_xpath('//*[@id="form:listaMunicipiosUF"]')
            cities.find_elements_by_tag_name('option')[0].click()
            cities.send_keys(Keys.SHIFT, Keys.END)

            driver.find_element_by_xpath('//*[@id="form:btnInserir"]').click()
            time.sleep(5)

            driver.find_element_by_xpath('//*[@id="form:botaoConsultar"]').click()
            time.sleep(30)
            print('Query done. ' + self._print_time())

            driver.find_element_by_xpath('//*[@id="form:botaoExportarCsv"]').click()
            time.sleep(20)
            print('Table downloaded. ' + self._print_time())

            self._rename_file(uf)

        except (WebDriverException, NoSuchElementException, NoSuchWindowException) as e:
            print(e)
        finally:
            driver.close()
            print('Browser closed. ' + self._print_time())

    def _rename_file(self, uf):
        try:
            file = self.dir + r'/relatorio_mei.csv'
            new_file = r'{}/{}_cnae_e_municipios_{}.csv'.format(
                self.dir, uf, self._print_time(now=False)
            )
            os.rename(file, new_file)
            print('File renamed ' + self._print_time())
        except FileExistsError as e:
            print(e)
            self._remove_garbage_files()
        except FileNotFoundError as e:
            print(e)

    def _print_time(self, now=True):
        timestamp = time.localtime(time.time())
        if now:
            ptime = '{}/{}/{} {}:{}:{}'.format(timestamp.tm_mday, timestamp.tm_mon, timestamp.tm_year,
                                               timestamp.tm_hour, timestamp.tm_min, timestamp.tm_sec)
            return ptime

        ptime = '{:04d}{:02d}{:02d}'.format(timestamp.tm_year, timestamp.tm_mon, timestamp.tm_mday)
        return ptime

    def _remove_garbage_files(self):
        files = os.listdir(self.dir)
        for file in files:
            if not file[:8] == 'mei_cnae':
                os.remove(self.dir + '/' + file)
