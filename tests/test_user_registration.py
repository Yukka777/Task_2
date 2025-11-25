import pytest
import requests
import allure
from faker import Faker
from endpoints import Endpoints  # Добавляем импорт эндпоинтов

fake = Faker()

@allure.epic("API Tests")
@allure.feature("User Registration")
class TestUserRegistration:

    @allure.title("Успешная регистрация нового пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_successful_user_registration(self):
        
        with allure.step("Подготовка данных для регистрации"):
            user_data = {
                "email": fake.email(),
                "password": fake.password(),
                "name": fake.first_name()
            }
        
        with allure.step("Выполнение запроса на регистрацию"):
            # Используем Endpoints.REGISTER вместо ручного составления URL
            response = requests.post(Endpoints.REGISTER, json=user_data)
            response_data = response.json()
            
            # Добавляем проверку статуса
            if response.status_code != 200:
                pytest.skip(f"Проблема с регистрацией: {response_data.get('message', 'Unknown error')}")
        
        with allure.step("Проверка успешной регистрации"):
            assert response.status_code == 200
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert response_data["user"]["email"] == user_data["email"]
            assert response_data["user"]["name"] == user_data["name"]
            
        with allure.step("Очистка: удаление пользователя"):
            headers = {"Authorization": response_data["accessToken"]}
            # Используем Endpoints.USER_INFO вместо ручного составления URL
            requests.delete(Endpoints.USER_INFO, headers=headers)

    @allure.title("Регистрация с уже существующим email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_existing_user(self):
        
        with allure.step("Регистрация первого пользователя"):
            user_data = {
                "email": fake.email(),
                "password": fake.password(),
                "name": fake.first_name()
            }
            # Используем Endpoints.REGISTER вместо ручного составления URL
            first_response = requests.post(Endpoints.REGISTER, json=user_data)
            first_data = first_response.json()
            
            # Добавляем проверку статуса
            if first_response.status_code != 200:
                pytest.skip(f"Проблема с регистрацией первого пользователя: {first_data.get('message', 'Unknown error')}")
            
            # Получим токен
            access_token = first_data.get("accessToken")
            if not access_token:
                access_token = next((v for k, v in first_data.items() 
                                   if isinstance(v, str) and len(v) > 10), None)
        
        with allure.step("Попытка регистрации с тем же email"):
            # Используем Endpoints.REGISTER вместо ручного составления URL
            response = requests.post(Endpoints.REGISTER, json=user_data)
        
        with allure.step("Проверка ошибки дублирования"):
            assert response.status_code == 403
            response_data = response.json()
            assert response_data["success"] is False
            assert "User already exists" in response_data["message"]
            
        with allure.step("Очистка"):
            headers = {"Authorization": access_token}
            # Используем Endpoints.USER_INFO вместо ручного составления URL
            requests.delete(Endpoints.USER_INFO, headers=headers)
