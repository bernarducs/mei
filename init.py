from selenium import webdriver


def config(path_folder: str, headless: bool):
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
