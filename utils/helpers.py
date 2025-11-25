import random
import string
from faker import Faker

fake = Faker()

def create_random_email():
    """Генерация случайного email"""
    return f"test_{random.randint(10000, 99999)}_{fake.email()}"

def create_random_password(length=12):
    """Генерация случайного пароля"""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for i in range(length))

def create_random_name():
    """Генерация случайного имени"""
    return fake.first_name()

def get_random_ingredients(api_session, base_url, count=2):
    """Получение случайных ингредиентов из API"""
    response = api_session.get(f"{base_url}/ingredients")
    ingredients_data = response.json()
    
    if "data" in ingredients_data:
        ingredients = ingredients_data["data"]
    else:
        ingredients = ingredients_data.get("ingredients", [])
    
    if len(ingredients) < count:
        raise Exception(f"Недостаточно ингредиентов. Доступно: {len(ingredients)}, требуется: {count}")
    
    return [ingredient["_id"] for ingredient in ingredients[:count]]
