import time
from selenium.webdriver.common.keys import Keys
from helpers import retorna_tabela


def municipio_cnae(driver, uf="PERNAMBUCO"):

    xpath_page = '/html/body/table/tbody/tr[2]/td/form/div/div/div[1]/ul/li[6]/a'
    xpath_listbox = '//*[@id="form:uf"]'
    xpath_municipios = '//*[@id="form:listaMunicipiosUF"]'
    xpath_btn_inserir = '//*[@id="form:btnInserir"]'
    xpath_btn_consulta = '//*[@id="form:botaoConsultar"]'
    xpath_tab_completa = '//*[@id="form:j_id62"]'

    # CNAE/MUNICIPIO
    page = driver.find_element_by_xpath(xpath_page)
    page.click()

    # selecionando UF na listbox
    time.sleep(2)
    el = driver.find_element_by_xpath(xpath_listbox)
    for option in el.find_elements_by_tag_name('option'):
        if option.text == uf:
            option.click()
            break

    time.sleep(2)
    cities = driver.find_element_by_xpath(xpath_municipios)

    time.sleep(5)
    cities.find_elements_by_tag_name('option')[0].click()
    cities.send_keys(Keys.SHIFT, Keys.END)

    driver.find_element_by_xpath(xpath_btn_inserir).click()
    time.sleep(2)

    tab_check = retorna_tabela(driver, xpath_btn_consulta, xpath_tab_completa)

    return tab_check
