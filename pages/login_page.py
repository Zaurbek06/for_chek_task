from asyncio import timeout
from locators.locators import LoginPageLocators as L
from pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        """Инициализирует страницу входа

        Args:
            page: Экземпляр страницы Playwright
        """
        super().__init__(page)
        self.L = L


    def login(self, email: str, password: str) ->None:
        """Выполняет вход в систему по email и паролю

        Args:
            email: Адрес электронной почты
            password: Пароль пользователя
        """
        self.go_to(L.url)
        self.wait_for(L.mail_input)
        self.wait_for(L.password_input)
        self.fill(L.mail_input, email)
        self.fill(L.password_input, password)
        self.click(L.button_log_in)
