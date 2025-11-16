from utils.helpers import generate_unique_email, generate_password, generate_username

class TestUserData:
    @staticmethod
    def get_valid_user_credentials():
        return {
            "email": generate_unique_email(),
            "password": generate_password(),
            "name": generate_username()
        }
    
    @staticmethod
    def get_invalid_emails():
        return [
            "invalid-email",
            "missing@domain",
            "@missingusername.com",
            "spaces in@email.com"
        ]
    
    @staticmethod
    def get_short_passwords():
        return ["123", "a", "p", "1"]
    
    @staticmethod
    def get_empty_fields_combinations():
        base_data = TestUserData.get_valid_user_credentials()
        combinations = []
        
        # Отсутствует email
        no_email = base_data.copy()
        no_email["email"] = ""
        combinations.append(no_email)
        
        # Отсутствует пароль
        no_password = base_data.copy()
        no_password["password"] = ""
        combinations.append(no_password)
        
        # Отсутствует имя
        no_name = base_data.copy()
        no_name["name"] = ""
        combinations.append(no_name)
        
        return combinations

class TestOrderData:
    @staticmethod
    def get_valid_order_payload(ingredient_ids):
        return {
            "ingredients": ingredient_ids
        }
    
    @staticmethod
    def get_invalid_order_payloads():
        return [
            {"ingredients": []},  # Пустой список
            {"ingredients": ["invalid_hash_123"]},  # Неверный хеш
            {"ingredients": ["123", "456"]},  # Несколько неверных хешей
            {}  # Отсутствует поле ingredients
        ]

class ErrorMessages:
    USER_EXISTS = "User already exists"
    REQUIRED_FIELDS = "Email, password and name are required fields"
    INVALID_CREDENTIALS = "email or password are incorrect"
    UNAUTHORIZED = "You should be authorised"
    INGREDIENTS_REQUIRED = "Ingredient ids must be provided"
    EMAIL_EXISTS = "User with such email already exists"