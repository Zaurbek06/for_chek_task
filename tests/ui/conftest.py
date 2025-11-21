import os

import pytest
from playwright.sync_api import sync_playwright, Browser

@pytest.fixture(scope="session")
def browser() -> Browser:
    """Запускает браузер Chromium для всех тестов в сессии

    Args:
        (нет внешних аргументов)

    Return:
        browser: Экземпляр запущенного браузера Chromium
    """
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, slow_mo=1000)
    yield browser
    browser.close()
    playwright.stop()




