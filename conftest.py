import pytest
from selenium import webdriver



def pytest_addoption(parser):
    parser.addoption('--browser_name', action ='store', default = "chrome",  # настраиваем определение параметров командной строки которые можем вводить
                    help = "Choose browser: chrome or firefox")
    parser.addoption("--language", action = "store", default = None,
                    help = "Choose language: en, ru and etc")

@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("browser_name")  # с помощью встроенной фикстуры request передаём браузеру параметры
    user_language = request.config.getoption("language")

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()  # если в терминале указали хром, запускается он
        options.add_experimental_option('excludeSwitches', ['enable-logging'])  # данная строка отключает логирование в консоли, убирает текст DevTools listening on ws://127.0.0.1 и прочий мусор
        options.add_experimental_option('prefs', {'intl.accept_languages': user_language})  # передаём аргумент языка
        options.add_argument('--start-maximized') # развернуть окно во весь экран
        #options.add_argument('--headless') # запуск браузера в скрытом режиме без отображения 
        #options.add_argument('window-size=1920,1080') # Размер окна запущенного браузера
        browser = webdriver.Chrome(options=options)  # присваиваем переменной options предыдущие значения options
        print("\nstart chrome browser for test..")
    elif browser_name == "firefox":
        fp = webdriver.FirefoxProfile()
        fp.set_preference("intl.accept_languages", user_language)
        browser = webdriver.Firefox(firefox_profile=fp)
        print("\nstart firefox browser for test..")
    else:
        # raise pytest.UsageError("--browser_name should be chrome or firefox")
        print("--browser_name should be chrome or firefox")
    yield browser
    print("\nquit browser..")
    browser.quit()

