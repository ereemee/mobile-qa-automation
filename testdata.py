"""
Sauce Labs 데모 앱 테스트 데이터 모음.
앱에서 제공하는 공개 테스트 계정·더미 결제 정보만 사용한다.
"""

# 계정
VALID_USER = {"username": "bod@example.com", "password": "10203040"}
LOCKED_USER = {"username": "alice@example.com", "password": "10203040"}

# 배송지
SHIPPING = {
    "full_name": "Rebecca Winter",
    "address1": "Mandorley 112",
    "city": "Truro",
    "zip": "89750",
    "country": "United Kingdom",
}

# 결제 정보 (더미)
PAYMENT = {
    "name": "Rebecca Winter",
    "card_number": "3258125675687891",
    "expiration": "0330",
    "cvv": "123",
}

# 기대 메시지
MSG_USERNAME_REQUIRED = "Username is required"
MSG_LOCKED_OUT = "Sorry this user has been locked out."
MSG_FULL_NAME_REQUIRED = "Please provide your full name."
MSG_PASSWORD_REQUIRED = "Enter Password"
