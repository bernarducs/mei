from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException, NoSuchWindowException
import time
from datetime import datetime
import os

path = os.getcwd() + '\\bases'
print(path)

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", path)
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv")
fp.set_preference("dom.disable_deforeunload", True)

options = webdriver.FirefoxOptions()
options.add_argument('-headless')

# geckodriver = 'C:\\Users\\User\\Downloads\\instaladores\\selenium\\geckodriver.exe'

while True:

    try:
        browser = webdriver.Firefox(fp, options=options)
        time.sleep(15)
        browser.get('http://www22.receita.fazenda.gov.br/inscricaomei/private/pages/relatorios/opcoesRelatorio.jsf#')
        print('Conectado.')
    except WebDriverException as e:
        print(e)
        continue

    try:
        # acessando a secao CNAE/MUNICIPIO
        # secao = browser.find_element_by_link_text('CNAE/Município')
        secao = browser.find_element_by_xpath('/html/body/table/tbody/tr[2]/td/form/div/div/div[1]/ul/li[6]/a')
        res = secao.click()

        # acessando e marcando PERNAMBUCO na listbox
        el = browser.find_element_by_xpath('//*[@id="form:uf"]')
    except NoSuchElementException as e:
        print(e)
        browser.close()
        continue
    except NoSuchWindowException as e:
        print(e)
        browser.close()
        continue

    for option in el.find_elements_by_tag_name('option'):
       if option.text == 'PERNAMBUCO':
            option.click()    # select() in earlier versions of webdriver
            break

    time.sleep(5)

    try:
        # marcando todos os MUNICIPIOS
        municipios = browser.find_element_by_xpath('//*[@id="form:listaMunicipiosUF"]')
        for municipio in municipios.find_elements_by_tag_name('option'):
            municipio.click()

        print('Municípios selecionados.')
        time.sleep(1)

        browser.find_element_by_xpath('//*[@id="form:btnInserir"]').click()
        time.sleep(1)

        browser.find_element_by_xpath('//*[@id="form:botaoConsultar"]').click()
        time.sleep(60)
        print('Consulta realizada.')

        try:
            consultar = browser.find_element_by_xpath('//*[@id="form:botaoExportarCsv"]').click()
            print('Arquivo exportado.')
            time.sleep(10)
        except NoSuchWindowException as e:
            print(e)
            continue

        browser.close()
    except NoSuchElementException as e:
        print(e)
        browser.close()
        continue
    except WebDriverException as e:
        print(e)
        browser.close()
        continue

    timestamp = time.localtime(time.time())
    ano = timestamp.tm_year
    mes = timestamp.tm_mon
    dia = timestamp.tm_mday

    try:
        os.rename(path + '\\relatorio_mei.csv', path + '\\mei_cnae_municipios_{:04d}{:02d}{:02d}.csv'.format(ano, mes, dia))
        print('Arquivo renomeado')
    except FileExistsError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)

    now = datetime.now()
    print('{}-{}-{} {}:{}:{}'.format(now.day, now.month, now.year, now.hour, now.minute, now.second))
    time.sleep(60 * 60)
