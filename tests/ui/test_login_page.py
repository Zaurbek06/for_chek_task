import os

import allure
from playwright.sync_api import expect, Browser
import pytest

from pages.login_page import LoginPage

@allure.feature('Login test')
@allure.story('Вход в систему')
def test_check_login(browser: Browser) ->None:
    """Проверяет успешный вход в систему по корректным учётным данным

    Args:
        browser: Экземпляр браузера
    """
    with allure.step('Open page'):
        page = browser.new_page()
    with allure.step('Вход по логину и паролю'):
        login = LoginPage(page)
        login.login('zaurbek.pugoev@bk.ru', 'Za2780246')
        page.wait_for_url('https://app.clickup.com/90151913392/v/l/2kyqj1xg*', timeout=90000)

@allure.feature('Login test')
@allure.story('Негативный тест входа в систему')
def test_negative_login(browser: Browser) -> None:
    """Проверяет отображение ошибки при входе с неверным паролем

    Args:
        browser: Экземпляр браузера
    """
    with allure.step('Open page'):
        page = browser.new_page()
    with allure.step('Вход в систему с неверным паролем'):
        login = LoginPage(page)
        login.login('zaurbek.pugoev@bk.ru', 'Za2780247')
        error = page.locator('.cu-password-input__error.ng-star-inserted')
        error.wait_for(state='visible', timeout=100000)
        expect(error).to_be_visible()
        expect(error).to_have_text('Incorrect password for this email.')

