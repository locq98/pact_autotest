import pytest
from selenium import webdriver


@pytest.fixture
def browser():
    print('\nstart browser for test...')
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.implicitly_wait(10)
    yield browser
    print('\nquit browser...')
    browser.quit()