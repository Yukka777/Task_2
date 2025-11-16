class Endpoints:
    BASE_URL = "https://stellarburgers.education-services.ru/api"
    
    # Auth endpoints
    REGISTER = f"{BASE_URL}/auth/register"
    LOGIN = f"{BASE_URL}/auth/login"
    LOGOUT = f"{BASE_URL}/auth/logout"
    USER_INFO = f"{BASE_URL}/auth/user"
    TOKEN_REFRESH = f"{BASE_URL}/auth/token"
    
    # Order endpoints
    ORDERS = f"{BASE_URL}/orders"
    ALL_ORDERS = f"{BASE_URL}/orders/all"
    INGREDIENTS = f"{BASE_URL}/ingredients"
    
    # Password endpoints
    PASSWORD_RESET = f"{BASE_URL}/password-reset"
    PASSWORD_RESET_CONFIRM = f"{BASE_URL}/password-reset/reset"