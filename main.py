from init import init_browser
from stats_reports import municipio_cnae
from helpers import verifica_arquivo, verifica_dir, retorna_ufs, \
    del_arquivos_inuteis, exporta_csv, renomeia_arquivo


def ufs_por_municipio_cnae(pasta):
    ufs = retorna_ufs()
    for uf in ufs:
        uf_por_municipio_cnae(pasta, uf=uf)


def uf_por_municipio_cnae(pasta, uf='PERNAMBUCO'):
    check = verifica_arquivo(pasta, uf)
    if not check:
        del_arquivos_inuteis(pasta)
        path_folder = verifica_dir(pasta)
        driver = init_browser(path_folder, headless=False)
        tab_check = municipio_cnae(driver, uf=uf)
        if tab_check:
            exporta_csv(driver)
            renomeia_arquivo(path_folder, uf)
        else:
            print(f"Não foi possível exportar {uf}")
        driver.quit()
    else:
        print(f"O arquivo {check} já existe.")

