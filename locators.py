"""
Sauce Labs 데모 앱 공통 locator 모음.
Appium Inspector / page source로 확인한 resource-id를 한 곳에서 관리한다.
"""

PKG = "com.saucelabs.mydemoapp.android:id/"

# 상품 목록 / 상세
PRODUCT_ID = PKG + "productIV"
ADD_TO_CART_ID = PKG + "cartBt"  # 상세 화면의 Add To Cart
CART_BADGE_ID = PKG + "cartTV"

# 장바구니
CART_ICON_ID = PKG + "cartRL"
CART_LIST_ID = PKG + "productRV"
PROCEED_ID = PKG + "cartBt"  # 장바구니 화면의 Proceed To Checkout (상세 화면과 id가 같음)

# 메뉴 / 로그인
MENU_ID = PKG + "menuIV"
USERNAME_ID = PKG + "nameET"
PASSWORD_ID = PKG + "passwordET"
LOGIN_BTN_ID = PKG + "loginBtn"
NAME_ERROR_ID = PKG + "nameErrorTV"
PASSWORD_ERROR_ID = PKG + "passwordErrorTV"

# 배송지
FULL_NAME_ID = PKG + "fullNameET"
ADDRESS1_ID = PKG + "address1ET"
CITY_ID = PKG + "cityET"
ZIP_ID = PKG + "zipET"
COUNTRY_ID = PKG + "countryET"
TO_PAYMENT_ID = PKG + "paymentBtn"  # 배송지 화면의 To Payment

# 결제 정보
CARD_NUMBER_ID = PKG + "cardNumberET"
CARD_NAME_ID = PKG + "nameET"  # 카드 소유자 이름 (로그인 아이디 입력란과 id가 같음)
EXPIRATION_ID = PKG + "expirationDateET"
CVV_ID = PKG + "securityCodeET"
