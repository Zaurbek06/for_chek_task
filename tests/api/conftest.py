import allure
import pytest
import requests
from utils.helpers import CLICKUP_API_KEY

BASE_URL = 'https://api.clickup.com/api/v2'

HEADERS = {
    "Authorization": CLICKUP_API_KEY,
    "Content-Type": "application/json"
}



@pytest.fixture
def create_task() -> None:
    """Создаёт временную задачу через API и возвращает её идентификатор

    Args:
        (нет внешних аргументов)

    Return:
        task_id: Идентификатор созданной задачи
    """
    with allure.step('Data create task'):
        list_id = '901517313290'
        task_data = {
            "name": "[AUTO] Временная задача для теста",
            "description": "Создана автоматическим тестом. Будет удалена.",
            "status": "to do"
        }
    with allure.step('Request create task'):
        response = requests.post(
            f"{BASE_URL}/list/{list_id}/task",
            headers=HEADERS,
            json=task_data
        )
    with allure.step('Check status code and get ID'):
        assert response.status_code == 200, f"❌ Не смог создать задачу: {response.text}"
        task = response.json()
        task_id = task["id"]
    with allure.step('Pass id to the function'):
        yield task_id
    with allure.step('Delete task'):
        delete_resp = requests.delete(
            f"{BASE_URL}/task/{task_id}",
            headers=HEADERS
        )

