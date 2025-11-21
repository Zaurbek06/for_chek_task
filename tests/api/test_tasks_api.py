import pytest
import requests
from utils.helpers import CLICKUP_API_KEY
from tests.api.conftest import BASE_URL, HEADERS
import allure


@allure.feature('Create task')
def test_create_task():
    with allure.step('Data for task'):
        task_data = {
            "name": "[AUTO] Временная задача для теста",
            "description": "Создана автоматическим тестом. Будет удалена.",
            "status": "to do"
        }
    with allure.step('Post request'):
        list_id = '901517313290'
        response = requests.post(f'{BASE_URL}/list/{list_id}/task', headers=HEADERS, json=task_data)
        assert response.status_code == 200
        task = response.json()
        task_id = task["id"]
    with allure.step('Delete creating task'):
        delete = requests.delete(f'{BASE_URL}/task/{task_id}', headers=HEADERS)
    with allure.step('Check status code'):
        assert delete.status_code == 204

@allure.feature('Get data')
def test_get_task(create_task):
    task_id = create_task
    with allure.step('Get request'):
        response = requests.get(f'{BASE_URL}/task/{task_id}', headers=HEADERS)
    with allure.step('Check status code'):
        assert response.status_code == 200

@allure.feature('Put data task')
def test_update_task(create_task):
    task_data = {
        "name": 'AUTO to TEST',
        "description": "Создана автоматическим тестом. NO Будет удалена.",
        "status": "to do"
    }
    task_id = create_task
    with allure.step('Put request'):
        resp = requests.put(f'{BASE_URL}/task/{task_id}', headers=HEADERS, json=task_data)
    with allure.step('Check status code'):
        assert resp.status_code == 200

@allure.feature('Delete task')
def test_delete_task(create_task):
    task_id = create_task
    with allure.step('Delete request'):
        response = requests.delete(f'{BASE_URL}/task/{task_id}', headers=HEADERS)
    with allure.step('Check status code'):
        assert response.status_code == 204

@allure.feature('Create task with invalid ID')
def test_invalid_create_task():
    with allure.step('invalid ID'):
        list_id = '901517313290'
    with allure.step('Create task with invalid ID'):
        response = requests.post(f'{BASE_URL}/list{list_id}', json={"name":""}, headers=HEADERS)
    with allure.step('Check status code'):
        assert response.status_code == 404

@allure.feature('Invalid get requests')
def test_get_invalid_task():
    with allure.step('invalid id'):
        invalid_id = 99999
    with allure.step('Get request'):
        response = requests.get(f'{BASE_URL}/task/{invalid_id}', headers=HEADERS)
    with allure.step('Check status code'):
        assert response.status_code == 401

@allure.feature('Update task with invalid ID')
def test_update_invalid_task():
    with allure.step('invalid id'):
        list_invalid_id = 99999
    with allure.step('data'):
        task_data = {
            "name": 'AUTO to TEST',
            "description": "Создана автоматическим тестом. Будет удалена.",
            "status": "to go DO"
        }
    with allure.step('Put request'):
        response = requests.put(f'{BASE_URL}/list{list_invalid_id}/task')
    with allure.step('Check status code'):
        assert response.status_code == 404

@allure.feature('Delete invalid task')
def test_delete_invalid_test():
    with allure.step('invalid id'):
        task_id = 1234
    with allure.step('delete request'):
        response = requests.delete(f'{BASE_URL}/task{task_id}', headers=HEADERS)
    with allure.step('Check status code'):
        assert response.status_code == 404

