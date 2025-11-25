import pytest
import requests
from urls import Urls
from helpers import create_random_email, create_random_password, create_random_name
import urllib3
import warnings
import os
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning

@pytest.fixture
def api_session():
    """
    Фикстура для API сессии с отключенной SSL проверкой
    """
    session = requests.Session()
    session.verify = False
    
    # Отключение предупреждений
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=3)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    return session

@pytest.fixture
def create_new_user_and_delete(api_session):
    """
    Фикстура для создания временного пользователя с автоматическим удалением после теста
    """
    # Генерация случайных учетных данных
    payload_cred = {
        'email': create_random_email(),
        'password': create_random_password(),
        'name': create_random_name()
    }
    
    # Регистрация пользователя
    response = api_session.post(Urls.USER_REGISTER, json=payload_cred)
    response_body = response.json()

    # Проверка успешной регистрации
    if response.status_code != 200 or 'accessToken' not in response_body:
        pytest.fail(f"Не удалось создать пользователя: {response.status_code} - {response_body}")

    # Возврат данных для использования в тестах
    yield payload_cred, response_body

    # Автоматическое удаление пользователя после теста
    access_token = response_body['accessToken']
    try:
        api_session.delete(Urls.USER_DELETE, headers={'Authorization': access_token})
    except Exception as e:
        print(f"Предупреждение: не удалось удалить пользователя: {e}")

@pytest.fixture
def authenticated_user(create_new_user_and_delete):
    """
    Фикстура для создания аутентифицированного пользователя
    Возвращает headers с токеном для использования в API запросах
    """
    user_data, response_body = create_new_user_and_delete
    access_token = response_body['accessToken']
    
    headers = {"Authorization": access_token}
    return {
        'user_data': user_data,
        'headers': headers,
        'access_token': access_token
    }
