import os

import allure
import pytest
import requests
from playwright.sync_api import Page


@pytest.fixture
def login_page_test(browser) ->Page:
    """Выполняет вход через UI и возвращает страницу после авторизации

        Args:
            browser: Экземпляр браузера

        Return:
            page: Страница после успешного входа
        """
    with allure.step('data Go to Clickup'):
        mail_input = '#login-email-input'
        password_input = '#login-password-input'
        button_log_in = '.login-page-v4_submit'
    with allure.step('Go to Clickup on LOGIN'):
        page = browser.new_page()
        page.goto('https://app.clickup.com/login', timeout=900000)
        page.wait_for_selector(mail_input, timeout=90000)
        page.wait_for_selector(password_input, timeout=90000)
        page.wait_for_selector(button_log_in, timeout=90000)
        page.fill(mail_input, 'zaurbek.pugoev@bk.ru', timeout=90000)
        page.fill(password_input, 'Za2780246', timeout=90000)
        page.click(button_log_in, timeout=90000)
        page.wait_for_url('https://app.clickup.com/90151913392/v/l/2kyqj1xg-475*', timeout=90000)
    with allure.step('Pass to page'):
        yield page
    with allure.step('Close page'):
        page.close()
    # page.wait_for_url('https://app.clickup.com/90151913392/v/l/2kyqj1xg-475?pr=90157968226', timeout=10000)


@pytest.fixture(scope="function")
def create_test_card() -> dict:
    """Создаёт тестовую задачу через API и возвращает её данные

    Args:
        (нет внешних аргументов)

    Return:
        task: Словарь с данными созданной задачи
    """
    import requests
    with allure.step('Data for created'):
        BASE_URL = 'https://api.clickup.com/api/v2'
        api_key = 'pk_254555049_SFOSPHULNOQODBT1ZOSJF8W885ROPC4R'
        list_id = '901517313290'
        headers = {"Authorization": api_key}
        payload = {"name": "Card for UI deletion test"}

    with allure.step('Create new card for UI deletion test'):
        resp = requests.post(f"{BASE_URL}/list/{list_id}/task", json=payload, headers=headers, timeout=80000)
        assert resp.status_code == 200
        task = resp.json()
        task_id = task["id"]
    with allure.step('Pass to the function'):
        yield task

    with allure.step('Удаляем на случай если UI не удалил'):
        try:
            requests.delete(f"https://api.clickup.com/api/v2/task/{task_id}", headers=headers)
        except Exception:
            pass  # Игнорируем ошибки при cleanup


@pytest.fixture(scope="function")
def delete_card_ui_api() -> None:
    """Обеспечивает пост-очистку: удаляет последнюю созданную задачу через API

    Args:
        (нет внешних аргументов)

    Return:
        None: Фикстура завершается без возврата значения
    """
    yield
    with allure.step('Get id created task and delete'):
        try:
            # Замените 'YOUR_ACCESS_TOKEN' на ваш токен доступа ClickUp
            access_token = 'pk_254555049_SFOSPHULNOQODBT1ZOSJF8W885ROPC4R'
            # Замените 'YOUR_SPACE_ID' на ID вашего пространства
            list_id = '901517313290'

            # Устанавливаем заголовки для запроса
            headers = {
                'Authorization': access_token,
            }

            # URL для получения задач в пространстве
            url = f'https://api.clickup.com/api/v2/list/{list_id}/task'

            with allure.step('Get request'):
                response = requests.get(url, headers=headers)

            with allure.step('Check status code'):
                assert response.status_code == 200
                tasks = response.json().get('tasks', [])

            with allure.step('Получаем ID последней задачи'):
                latest_task = max(tasks, key=lambda task: task['date_created'])
                task_id = latest_task['id']
            with allure.step('Удаляем последнюю созданную задачу по ID'):
                response = requests.delete(f'https://api.clickup.com/api/v2/task/{task_id}', headers=headers)
            with allure.step('Check status code'):
                assert response.status_code in (204, 200)
        except Exception as e:
            print(f"⚠️ Cleanup failed: {e}")
