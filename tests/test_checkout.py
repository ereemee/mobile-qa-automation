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
ADDRESS1_ID = PKG + "address1ET"
CITY_ID = PKG + "cityET"
ZIP_ID = PKG + "zipET"
COUNTRY_ID = PKG + "countryET"
TO_PAYMENT_ID = PKG + "paymentBtn"  # 배송지 화면의 To Payment
CARD_NUMBER_ID = PKG + "cardNumberET"  # 결제 화면 카드 번호 입력란
CARD_NAME_ID = PKG + "nameET"  # 결제 화면 카드 소유자 이름 (Inspector로 확인)
EXPIRATION_ID = PKG + "expirationDateET"  # 유효기간 (Inspector로 확인)
CVV_ID = PKG + "securityCodeET"  # CVV (Inspector로 확인)


def test_checkout_requires_login(driver):
    """비로그인 상태로 결제를 진행하면 로그인 후 배송지 입력 화면으로 이동하는지 확인"""
    wait = go_to_shipping(driver)
    full_name = wait.until(EC.visibility_of_element_located((AppiumBy.ID, FULL_NAME_ID)))
    assert full_name.is_displayed()


def go_to_shipping(driver):
    """상품 담기 → 장바구니 → Proceed To Checkout → 로그인까지 진행하고 wait를 돌려준다"""
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((AppiumBy.ID, PRODUCT_ID)))[0].click()
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, ADD_TO_CART_ID))).click()
    wait.until(EC.text_to_be_present_in_element((AppiumBy.ID, CART_BADGE_ID), "1"))

    driver.find_element(AppiumBy.ID, CART_ICON_ID).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, CART_LIST_ID)))
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, PROCEED_ID))).click()

    username = wait.until(EC.element_to_be_clickable((AppiumBy.ID, USERNAME_ID)))
    username.send_keys("bod@example.com")
    driver.find_element(AppiumBy.ID, PASSWORD_ID).send_keys("10203040")
    driver.find_element(AppiumBy.ID, LOGIN_BTN_ID).click()
    return wait


def scroll_to_text(driver, text):
    """화면을 스크롤해서 text가 보이게 하고 그 요소를 돌려준다"""
    if driver.is_keyboard_shown():
        driver.hide_keyboard()
    return driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        "new UiScrollable(new UiSelector().scrollable(true))"
        f'.scrollIntoView(new UiSelector().text("{text}"))',
    )


def fill_shipping(driver, wait):
    """배송지를 입력하고 To Payment를 눌러 결제 정보 화면으로 이동한다"""
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, FULL_NAME_ID))).send_keys("Rebecca Winter")
    driver.find_element(AppiumBy.ID, ADDRESS1_ID).send_keys("Mandorley 112")
    driver.find_element(AppiumBy.ID, CITY_ID).send_keys("Truro")
    driver.find_element(AppiumBy.ID, ZIP_ID).send_keys("89750")
    driver.find_element(AppiumBy.ID, COUNTRY_ID).send_keys("United Kingdom")
    scroll_to_text(driver, "To Payment")
    driver.find_element(AppiumBy.ID, TO_PAYMENT_ID).click()


def test_shipping_to_payment(driver):
    """배송지를 입력하고 To Payment를 누르면 결제 정보 화면으로 이동하는지 확인"""
    wait = go_to_shipping(driver)
    fill_shipping(driver, wait)
    card = wait.until(EC.visibility_of_element_located((AppiumBy.ID, CARD_NUMBER_ID)))
    assert card.is_displayed()


def test_checkout_complete(driver):
    """결제 정보를 입력하고 주문하면 Checkout Complete 화면이 보이는지 확인"""
    wait = go_to_shipping(driver)
    fill_shipping(driver, wait)

    wait.until(EC.element_to_be_clickable((AppiumBy.ID, CARD_NAME_ID))).send_keys("Rebecca Winter")
    driver.find_element(AppiumBy.ID, CARD_NUMBER_ID).send_keys("3258125675687891")
    driver.find_element(AppiumBy.ID, EXPIRATION_ID).send_keys("0330")
    driver.find_element(AppiumBy.ID, CVV_ID).send_keys("123")

    scroll_to_text(driver, "Review Order").click()
    wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Place Order")')
        )
    ).click()

    complete = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Checkout Complete")')
    assert wait.until(EC.visibility_of_element_located(complete))
