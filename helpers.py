import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.common.exceptions import TimeoutException
from print_time import print_timestamp


def retorna_xpath(driver, timeout, freq, xpath):
    wbw = WebDriverWait(driver=driver, timeout=timeout, poll_frequency=freq)
    wbw.until(presence_of_element_located((By.XPATH, xpath)), "Elemento não encontrado.")
    return driver.find_element_by_xpath(xpath)


def retorna_tabela(driver, xpath_btn_consulta, xpath_tab_completa):
    print('Extraindo tabela.', print_timestamp())
    tentativas = [1, 2, 3]
    for i in tentativas:
        print(f"Tentativa {i} de 3...")
        driver.find_element_by_xpath(xpath_btn_consulta).click()
        try:
            retorna_xpath(driver, 150, 5, xpath_tab_completa)
            print('Tabela carregada.', print_timestamp())
            return True
        except TimeoutException as e:
            print('Tabela não foi carregada.')
    return False


def retorna_ufs():
    with open('lista de uf.txt', 'r', encoding='latin-1') as f:
        file = f.readlines()
    ufs = [uf[:-1] for uf in file]
    return ufs


def verifica_dir(name_folder):
    if not os.path.exists(name_folder):
        os.mkdir(name_folder)
        print(f"Arquivos baixados ficarão na pasta {name_folder}.")
    return os.path.join(os.getcwd(), name_folder)


def del_arquivos_inuteis(name_folder):
    for file in os.listdir(name_folder):
        if file[:13] == 'relatorio_mei':
            os.remove(os.path.join(name_folder, file))


def renomeia_arquivo(name_folder, uf):
    file = r'relatorio_mei.csv'
    if file in os.listdir(name_folder):
        old_file = os.path.join(name_folder, file)
        new_file = r'{}_cnae_e_municipios_{}.csv'.format(
            uf, print_timestamp(now=False)
        )
        new_file = os.path.join(name_folder, new_file)
        try:
            os.rename(old_file, new_file)
            print(f"Arquivo renomeado para {new_file} " + print_timestamp())
        except FileExistsError:
            print("Arquivo já existe.")


def verifica_arquivo(name_folder, uf):
    data = print_timestamp(now=False)
    name = f"{uf}_cnae_e_municipios_{data}.csv"
    if name in os.listdir(name_folder):
        return name
    else:
        return False


def exporta_csv(driver):
    xpath_btn_exportar = '//*[@id="form:botaoExportarCsv"]'
    driver.find_element_by_xpath(xpath_btn_exportar).click()
    time.sleep(10)
    print('Download concluído.', print_timestamp())
