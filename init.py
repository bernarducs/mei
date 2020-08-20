from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from print_time import print_timestamp
from helpers import retorna_xpath


def config(path_folder, headless=True):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", path_folder)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv")
    fp.set_preference("dom.disable_beforeunload", True)
    fp.set_preference("browser.download.manager.closeWhenDone", True)

    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument('-headless')

    driver = webdriver.Firefox(fp, options=options)

    return driver


def init_browser(files_dir, headless=True):
    url = 'http://www22.receita.fazenda.gov.br/inscricaomei/private/pages/relatorios/opcoesRelatorio.jsf#'
    xpath = '/html/body/table/tbody/tr[2]/td/form/div/div/div[1]/p'

    while True:
        driver = config(files_dir, headless=headless)
        try:
            driver.get(url)
            print('Browser iniciado. ' + print_timestamp())
            retorna_xpath(driver, 15, 5, xpath)
            break
        except TimeoutException as e:
            driver.quit()
            print(e)

    return driver
