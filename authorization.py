from telnetlib import EC
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import randint


class TestAuthorization():
    #Авторизация под валидным номером телефона/email и паролем.
    @pytest.mark.parametrize('logins', ['+78001002030', '88001002030', 'dalil53378@robhung.com'])
    @pytest.mark.authorization
    def test_authorization_with_valid_data_number_or_email_and_pass(self, browser, logins):
        login_link = 'https://msg.pact.im/login'
        browser.get(login_link)
        browser.execute_script("document.getElementById('carrot-messenger-collapsed-frame').style.visibility = 'hidden';")
        browser.find_element(By.XPATH, '//*[@id="ember4"]').send_keys(logins)
        browser.find_element(By.XPATH, '//*[@id="ember6"]').send_keys('111111')
        WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[3]/form/input[3]')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/form/input[3]').click()
        #проверяем корректность url при переходе и вводим текст в поиск, чтобы проверить отображение страницы
        time.sleep(10)
        assert 'https://msg.pact.im/messages?current_conversation_id' in browser.current_url, 'открывается некорректная ссылка'

    @pytest.mark.parametrize('numbers', ['8001002030', 'номерТелефона', 'TelephoneNumber', '-78001002030'])
    def test_authorization_with_invalid_format_number(self, browser, numbers):
        #Попытки авторизации с номером: 1. без +7 или 8, 2. логин русскими/латинскими буквами, 3. Вместо + использовать -
        login_link = 'https://msg.pact.im/login'
        browser.get(login_link)
        browser.execute_script("document.getElementById('carrot-messenger-collapsed-frame').style.display = 'none';")
        browser.find_element(By.XPATH, '//*[@id="ember4"]').send_keys(numbers)
        browser.find_element(By.XPATH, '//*[@id="ember6"]').send_keys('111111')
        WebDriverWait(browser, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[3]/form/input[3]')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/form/input[3]').click()
        WebDriverWait(browser, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'login-form-fail')))
        assert 'Пользователь с таким логином и паролем не существует' in \
               browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div').text, 'авторизация происходит с невалидными данными'

    def test_registration_with_valid_data(self, browser):
        #Регистрация аккаунта с валидными данными без успешного прохождения смс верификации на второй странице.
        random_int = randint(1000, 15000)
        random_numbers = randint(1000000, 9999999)
        random_email = f'ya.strokov+{random_int}@gmail.com'
        reg_link = 'https://msg.pact.im/signup'
        browser.get(reg_link)
        browser.execute_script("document.getElementById('carrot-messenger-collapsed-frame').style.display = 'none';")
        browser.find_element(By.ID, 'ember4').send_keys(f'Яростав_Автотест{random_int}')
        browser.find_element(By.XPATH, '//*[@id="ember5"]').send_keys(f'+7800{random_numbers}')
        browser.find_element(By.XPATH, '//*[@id="ember6"]').send_keys(random_email)
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/form/input[5]')))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/form/input[5]').click()
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.ID, 'ember15')))
        browser.find_element(By.ID, 'ember15').send_keys('12345')
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/form/div[2]/button').click()
        valid_text =  WebDriverWait(browser, 20).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[1]/div/div/div[3]/div'))).text
        assert 'Введенный код не совпадает с высланным' in valid_text, 'Ошибка на странице ввода смс'




