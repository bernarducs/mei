import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException, NoSuchWindowException
from helpers import retorna_tabela
from print_time import print_timestamp


def municipio_cnae(driver, uf="PERNAMBUCO"):

    xpath_page = '/html/body/table/tbody/tr[2]/td/form/div/div/div[1]/ul/li[6]/a'
    xpath_listbox = '//*[@id="form:uf"]'
    xpath_municipios = '//*[@id="form:listaMunicipiosUF"]'
    xpath_relatorio = '//*[@id="form:listaMunicipiosRelatorio"]'
    xpath_btn_inserir = '//*[@id="form:btnInserir"]'
    xpath_btn_consulta = '//*[@id="form:botaoConsultar"]'
    xpath_tab_completa = '//*[@id="form:j_id62"]'

    print(f"Extraindo {uf}.", print_timestamp())

    try:
        # CNAE/MUNICIPIO
        page = driver.find_element_by_xpath(xpath_page)
        page.click()

        # selecionando UF na listbox
        time.sleep(5)
        el = driver.find_element_by_xpath(xpath_listbox)
        for option in el.find_elements_by_tag_name('option'):
            if option.text == uf:
                option.click()
                break

        for tries in [1, 2, 3]:
            print(f"Carregando municípios. Tentativa {tries}/3.", print_timestamp())
            time.sleep(5)
            # verifica se a 1a listbox está preenchida
            cities = driver.find_element_by_xpath(xpath_municipios)
            n_cities = len(cities.text.split('\n'))
            if n_cities > 1 or cities.text == 'BRASILIA':
                cities.find_elements_by_tag_name('option')[0].click()
                cities.send_keys(Keys.SHIFT, Keys.END)
                driver.find_element_by_xpath(xpath_btn_inserir).click()
                time.sleep(5)
                # verifica se a 2a listbox está preenchida
                rel = driver.find_element_by_xpath(xpath_relatorio)
                n_rel = len(rel.text.split('\n'))
                if n_rel > 1 or rel.text == 'BRASILIA':
                    print("Municipíos carregados.")
                    break
            # se nao atenderem as condições
            if n_cities <= 1 and tries == 3:
                print("Não foi possível carregar os municípios.")
                return False
        time.sleep(2)
        tab_check = retorna_tabela(driver, xpath_btn_consulta, xpath_tab_completa)
    except (NoSuchElementException, WebDriverException, NoSuchWindowException) as e:
        print(e)
        return False
    return tab_check
