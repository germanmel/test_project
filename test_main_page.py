import time
from .pages.main_page import MainPage, url

def test_open_site(browser):
    page = MainPage(browser, url)
    time.sleep(5)
    page.check_js()

  