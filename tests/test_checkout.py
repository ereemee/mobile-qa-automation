from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PKG = "com.saucelabs.mydemoapp.android:id/"
PRODUCT_ID = PKG + "productIV"
ADD_TO_CART_ID = PKG + "cartBt"  # 상세 화면의 Add To Cart
CART_BADGE_ID = PKG + "cartTV"
CART_ICON_ID = PKG + "cartRL"
CART_LIST_ID = PKG + "productRV"
PROCEED_ID = PKG + "cartBt"  # 장바구니 화면의 Proceed To Checkout (상세 화면과 id가 같음)
USERNAME_ID = PKG + "nameET"
PASSWORD_ID = PKG + "passwordET"
LOGIN_BTN_ID = PKG + "loginBtn"
FULL_NAME_ID = PKG + "fullNameET"


def test_checkout_requires_login(driver):
    """비로그인 상태로 결제를 진행하면 로그인 후 배송지 입력 화면으로 이동하는지 확인"""
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((AppiumBy.ID, PRODUCT_ID)))[0].click()
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, ADD_TO_CART_ID))).click()
    wait.until(EC.text_to_be_present_in_element((AppiumBy.ID, CART_BADGE_ID), "1"))

    driver.find_element(AppiumBy.ID, CART_ICON_ID).click()
    # 상세 화면의 cartBt와 헷갈리지 않도록 장바구니 목록이 뜬 뒤에 누른다
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, CART_LIST_ID)))
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, PROCEED_ID))).click()

    # 결제 진행 시 로그인 화면이 뜸 → 로그인
    username = wait.until(EC.element_to_be_clickable((AppiumBy.ID, USERNAME_ID)))
    username.send_keys("bod@example.com")
    driver.find_element(AppiumBy.ID, PASSWORD_ID).send_keys("10203040")
    driver.find_element(AppiumBy.ID, LOGIN_BTN_ID).click()

    # 로그인 후 배송지 입력 화면(Full Name 입력란)으로 이동했는지 확인
    full_name = wait.until(EC.visibility_of_element_located((AppiumBy.ID, FULL_NAME_ID)))
    assert full_name.is_displayed()
