from hashlib import new
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException, TimeoutException, WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from termcolor import colored

class BasePage():

    # Инициализация драйвера(запуск браузера) при каждом объявлении экземпляра класса
    def __init__(self, browser, url, timeout=10): 
        self.browser = browser
        self.url = url
        self.browser.get(url)
        self.browser.implicitly_wait(timeout) 
        

    # Переход на нужную страницу(url)
    def open_page(self, url):
        self.browser.get(url)

    # Возврат назад 
    def go_back(self):
        self.browser.back()

    # Переход вперёд
    def go_forward(self):
        self.browser.forward()

    # Обновление страницы
    def refresh(self):
        self.browser.refresh()

    # Скрол страницы вниз, в offset указываем в пикселях до какого уровня делать скролл, иначе max
    def scroll_down(self, offset=0):
        if offset:
            self.browser.execute_script('window.scrollTo(0, {0});'.format(offset))
        else:
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    # Скрол страницы вниз, в offset указываем в пикселях до какого уровня делать скролл иначе max 
    def scroll_up(self, offset=0):
        if offset:
            self.browser.execute_script('window.scrollTo(0, {0});'.format(offset))
        else:
            self.browser.execute_script('window.scrollTo(0, -document.body.scrollHeight);')  

    # Скриншот отображаемой области страницы
    def screenshot(self, file_name= time.strftime("%d_%m_%Y-%H_%M_%S") + ".png"):
        self.browser.save_screenshot(f'E:\\Git\\test_project\\screenshots\\{file_name}')
   
    # Скриншот отображаемой области страницы без полос навигации
    def screenshot_no_scrollbar(self, file_name= time.strftime("%d_%m_%Y-%H_%M_%S") + ".png"):
        element = self.browser.find_element(By.XPATH, "/html/body")
        element.screenshot(f'E:\\Git\\test_project\\screenshots\\{file_name}')

    # Скриншот с указанным размером, принимает ширину и высоту экрана в пикселях
    def screenshot_set_size(self, width, height, file_name = time.strftime("%d_%m_%Y-%H_%M_%S") + '.png'):
            self.browser.set_window_size(width, height)
            element = self.browser.find_element(By.TAG_NAME, "body")
            element.screenshot(f'E:\\Git\\test_project\\screenshots\\{width}-{height}-{file_name}')

    # Полноразмерный скриншот всей страницы(весь макет страницы), работает только в headless режиме
    def full_screenshot2(self, file_name = "full-" + time.strftime("%d_%m_%Y-%H_%M_%S") + '.png'):
        original_size = self.browser.get_window_size()
        required_width = self.browser.execute_script('return document.body.parentNode.scrollWidth')
        required_height = self.browser.execute_script('return document.body.parentNode.scrollHeight')
        self.browser.set_window_size(required_width, required_height)
        self.browser.find_element(By.TAG_NAME, "body").screenshot(f'E:\\Git\\test_project\\screenshots\\{file_name}')
        self.browser.set_window_size(original_size['width'], original_size['height'])

    # Перейти на iframe по его имени
    def switch_to_iframe(self, iframe):
        self.browser.switch_to.frame(iframe)

    # Выйти из iframe
    def switch_out_iframe(self):
        self.browser.switch_to.default_content()

    # Получить текущий url страницы
    def get_current_url(self):
        return self.browser.current_url

    # Получить body страницы в html файл
    def get_body(self):
        source = ''
        try:
            source = self.browser.page_source
            with open('E:\\Git\\test_project\\files\\body.html', 'w', encoding="utf-8") as file:
                file.write(source)
        except:
            print(colored('Can not get page source', 'red'))
    
    # Проверка на js ошибки на странице - не работает
    def check_js_errors(self, ignore_list=None):

        ignore_list = ignore_list or []

        logs = self.browser.get_log('browser')
        for log_message in logs:
            if log_message['level'] != 'WARNING':
                ignore = False
                for issue in ignore_list:
                    if issue in log_message['message']:
                        ignore = True
                        break

                assert ignore, 'JS error "{0}" on the page!'.format(log_message)
        

            
   

