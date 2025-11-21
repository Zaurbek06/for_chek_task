from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page: Page) ->None:
        """Инициализирует базовую страницу

        Args:
            page:Экземпляр страницы Playwright
        """
        self.page = page

    def click(self, selector:str) -> None:
        """Выполняет клик по элементу

        Args:
           selector: CSS-селектор элемента

        """
        self.page.click(selector)

    def fill(self, selector:str, value:str) -> None:
        """Заполняет поле ввода текстом

        Args:
            selector: CSS-селектор поля ввода
            value: Текст для ввода
        """
        self.page.fill(selector, value)

    def wait_for(self, selector:str) -> None:
        """Ожидает появления элемента на странице

        Args:
            selector: CSS-селектор ожидаемого элемента
        """
        self.page.wait_for_selector(selector)

    def go_to(self, url: str) -> None:
        """Переходит по указанному url

        Args:
            url: Адрес страницы
        """
        self.page.goto(url, timeout=90000, wait_until="domcontentloaded")
        self.page.wait_for_load_state('load', timeout=90000)


    def locator(self, text: str) -> Locator:
        """Возвращает локатор элемента по селектору или тексту

        Args:
            text: Селектор или текст для поиска элемента

        Return:
            locator_obj: Объект локатора Playwright
        """
        locator_obj = self.page.locator(text)
        return locator_obj