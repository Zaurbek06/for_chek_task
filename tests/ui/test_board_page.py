import os

import allure
import requests
from playwright.sync_api import expect

@allure.feature('Create task and delete')
@allure.story('Create task API delete UI')
def test_delete_card_ui(login_page_test, create_test_card):
    """Удаляет задачу, созданную через API, с помощью UI

    Args:
        login_page_test: Фикстура с авторизованной страницей
        create_test_card: Фикстура с данными созданной задачи
    """
    page = login_page_test
    task = create_test_card["id"]
    team_id = os.getenv("TEAM_ID")

    with allure.step('Open List'):
        page.goto(f"https://app.clickup.com/90151913392/v/l/2kyqj1xg-475", timeout=120000)
    with allure.step('Open Task API'):
        card = page.locator('[data-test="task-row-main__link-text__Card for UI deletion test"]')
        expect(card).to_be_visible(timeout=140000)
        page.click('[data-test="task-row-main__link-text__Card for UI deletion test"]')
    with allure.step('Open settings and delete'):
        settings = page.locator('[data-test="task-view-header__task-settings"]')
        expect(settings).to_be_visible(timeout=140000)
        page.click('[data-test="task-view-header__task-settings"]')
        delete_button = page.locator('[data-test="dropdown-list-item__cu-task-view-menu-delete"]')
        expect(delete_button).to_be_visible(timeout=70000)
        delete_button.click()
    with allure.step('Check task is not visible'):
        expect(card).not_to_be_visible(timeout=100000)


@allure.feature('Create task and delete')
@allure.story('Create task UI delete API')
def test_delete_card_api(login_page_test, delete_card_ui_api) -> None:
    """Создаёт задачу через UI; удаление выполняется в фикстуре через API

    Args:
        login_page_test: Фикстура с авторизованной страницей
        delete_card_ui_api: Фикстура пост-очистки через API
    """
    task_name = 'Task delete card'
    with allure.step('Open List'):
        page = login_page_test
    with allure.step('Looking button add task'):
        add_button = page.locator('[data-test="task-list-footer-quick-task"]')
        expect(add_button).to_be_visible(timeout=120000)
        add_button.click()
    with allure.step('Task name'):
        input_fill = page.locator('[data-test="task-row-new__input"]')
        expect(input_fill).to_be_visible(timeout=120000)
        input_fill.fill(task_name)
    with allure.step('Save new task'):
        page.get_by_role("button", name="Save").click()
        card = page.locator('[data-test="task-row__container__Task delete card"]')
        expect(card).to_be_visible(timeout=100000)



