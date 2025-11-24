import pytest
import requests
import allure
from faker import Faker

fake = Faker()

@allure.epic("API Tests")
@allure.feature("User Authentication")
class TestUserAuthentication:

    def _register_user(self, base_url):
        """Вспомогательная функция для регистрации пользователя"""
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                user_data = {
                    "email": fake.email(),
                    "password": "testpassword123",
                    "name": fake.first_name()
                }
                response = requests.post(f"{base_url}/auth/register", json=user_data, timeout=10)
                response_data = response.json()
                
                if response.status_code == 200 and "accessToken" in response_data:
                    return response_data["accessToken"], user_data
                elif response.status_code == 403:
                    # Пользователь уже существует, пробуем с другим email
                    continue
                else:
                    # Другая ошибка, пробуем снова
                    continue
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                continue
        raise Exception("Не удалось зарегистрировать пользователя после нескольких попыток")

    @allure.title("Успешный вход в систему")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_successful_login(self, base_url):
        
        with allure.step("Регистрация пользователя"):
            access_token, user_data = self._register_user(base_url)
        
        with allure.step("Вход в систему"):
            login_data = {
                "email": user_data["email"],
                "password": user_data["password"]
            }
            response = requests.post(f"{base_url}/auth/login", json=login_data)
        
        with allure.step("Проверка успешного входа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] is True
            assert "accessToken" in response_data
            assert response_data["user"]["email"] == user_data["email"]
            
        with allure.step("Очистка"):
            try:
                headers = {"Authorization": access_token}
                requests.delete(f"{base_url}/auth/user", headers=headers)
            except:
                pass

    @allure.title("Вход с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self, base_url):
        
        with allure.step("Попытка входа с неверными данными"):
            login_data = {
                "email": "nonexistent@example.com",
                "password": "wrongpassword"
            }
            response = requests.post(f"{base_url}/auth/login", json=login_data)
        
        with allure.step("Проверка ошибки аутентификации"):
            assert response.status_code == 401
            response_data = response.json()
            assert response_data["success"] is False

            assert "email or password are incorrect" in response_data["message"]
