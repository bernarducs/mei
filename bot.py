import os

from selenium.common.exceptions import NoSuchElementException, \
    WebDriverException, NoSuchWindowException

from init import config
from mei import MeiCnaeMunicipio
from helpers import retorna_ufs


def ufs_por_municipio_cnae(pasta="arquivos", invisivel=True):
    ufs = retorna_ufs()
    for uf in ufs:
        uf_por_municipio_cnae(uf=uf, pasta=pasta, invisivel=invisivel)


def uf_por_municipio_cnae(uf="PERNAMBUCO", pasta="arquivos", invisivel=True):
    path_file = os.path.join(os.getcwd(), pasta)
    driver = config(path_file, headless=invisivel)
    mei = MeiCnaeMunicipio(driver, path_file, uf)
    file = mei.verifica_arquivo()
    if not file:
        mei.del_arquivos_inuteis()
        try:
            mei.abre_browser()
            mei.carrega_pagina_relatorio(mei.xpath_page)
            mei.uf_listbox(mei.xpath_listbox)
            checkbox = mei.verifica_listbox_municipios()
            if checkbox:
                table = mei.retorna_tabela(mei.xpath_btn_consulta,
                                           mei.xpath_tab_completa)
                if table:
                    mei.exporta_csv()
                    mei.renomeia_arquivo()
                else:
                    print(f"Não foi possível exportar o arquivo")
            else:
                print(f"Não foi possível exportar o arquivo.")
            driver.quit()
        except (NoSuchElementException, WebDriverException,
                NoSuchWindowException) as e:
            print(e)
            driver.quit()
            print("Não foi possível exportar o arquivo.")
    else:
        print(f"O arquivo {file} já existe.")
