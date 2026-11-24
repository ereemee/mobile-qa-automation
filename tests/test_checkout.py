from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators import (
    ADD_TO_CART_ID,
    ADDRESS1_ID,
    CARD_NAME_ID,
    CARD_NUMBER_ID,
    CART_BADGE_ID,
    CART_ICON_ID,
    CART_LIST_ID,
    CITY_ID,
    COUNTRY_ID,
    CVV_ID,
    EXPIRATION_ID,
    FULL_NAME_ERROR_ID,
    FULL_NAME_ID,
    LOGIN_BTN_ID,
    PROCEED_ID,
    PRODUCT_ID,
    TO_PAYMENT_ID,
    ZIP_ID,
)
from pages.login_page import LoginPage
from testdata import MSG_FULL_NAME_REQUIRED, PAYMENT, SHIPPING, VALID_USER


def add_to_cart_and_checkout(driver):
    """상품 담기 → 장바구니 → Proceed To Checkout까지 진행하고 wait를 돌려준다"""
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((AppiumBy.ID, PRODUCT_ID)))[0].click()
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, ADD_TO_CART_ID))).click()
    wait.until(EC.text_to_be_present_in_element((AppiumBy.ID, CART_BADGE_ID), "1"))

    driver.find_element(AppiumBy.ID, CART_ICON_ID).click()
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, CART_LIST_ID)))
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, PROCEED_ID))).click()
    return wait


def go_to_shipping(driver):
    """비로그인 상태로 결제를 진행하고, 나타난 로그인 화면에서 로그인까지 한다"""
    wait = add_to_cart_and_checkout(driver)
    LoginPage(driver).login(VALID_USER["username"], VALID_USER["password"])
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
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, FULL_NAME_ID))).send_keys(
        SHIPPING["full_name"]
    )
    driver.find_element(AppiumBy.ID, ADDRESS1_ID).send_keys(SHIPPING["address1"])
    driver.find_element(AppiumBy.ID, CITY_ID).send_keys(SHIPPING["city"])
    driver.find_element(AppiumBy.ID, ZIP_ID).send_keys(SHIPPING["zip"])
    driver.find_element(AppiumBy.ID, COUNTRY_ID).send_keys(SHIPPING["country"])
    scroll_to_text(driver, "To Payment")
    driver.find_element(AppiumBy.ID, TO_PAYMENT_ID).click()


def test_checkout_requires_login(driver):
    """비로그인 상태로 결제를 진행하면 로그인 후 배송지 입력 화면으로 이동하는지 확인"""
    wait = go_to_shipping(driver)
    full_name = wait.until(EC.visibility_of_element_located((AppiumBy.ID, FULL_NAME_ID)))
    assert full_name.is_displayed()


def test_checkout_when_logged_in(driver):
    """로그인 상태로 결제를 진행하면 로그인 화면 없이 배송지 입력 화면으로 이동하는지 확인"""
    page = LoginPage(driver).open_from_menu()
    page.login(VALID_USER["username"], VALID_USER["password"])
    page.wait_for_product_list()
    wait = add_to_cart_and_checkout(driver)
    full_name = wait.until(EC.visibility_of_element_located((AppiumBy.ID, FULL_NAME_ID)))
    assert full_name.is_displayed()
    # 로그인 화면을 거치지 않았는지 확인
    assert not driver.find_elements(AppiumBy.ID, LOGIN_BTN_ID)


def test_shipping_required_fields(driver):
    """배송지를 비우고 To Payment를 누르면 필수값 에러가 보이는지 확인"""
    wait = go_to_shipping(driver)
    wait.until(EC.visibility_of_element_located((AppiumBy.ID, FULL_NAME_ID)))
    scroll_to_text(driver, "To Payment")
    driver.find_element(AppiumBy.ID, TO_PAYMENT_ID).click()

    # 에러 TextView는 처음엔 invisible일 수 있으므로 visibility로 기다림
    error = wait.until(EC.visibility_of_element_located((AppiumBy.ID, FULL_NAME_ERROR_ID)))
    assert error.text == MSG_FULL_NAME_REQUIRED
    # 결제 정보 화면으로 넘어가지 않았는지도 확인
    assert not driver.find_elements(AppiumBy.ID, CARD_NUMBER_ID)


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

    wait.until(EC.element_to_be_clickable((AppiumBy.ID, CARD_NAME_ID))).send_keys(PAYMENT["name"])
    driver.find_element(AppiumBy.ID, CARD_NUMBER_ID).send_keys(PAYMENT["card_number"])
    driver.find_element(AppiumBy.ID, EXPIRATION_ID).send_keys(PAYMENT["expiration"])
    driver.find_element(AppiumBy.ID, CVV_ID).send_keys(PAYMENT["cvv"])

    scroll_to_text(driver, "Review Order").click()
    wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Place Order")')
        )
    ).click()

    complete = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Checkout Complete")')
    assert wait.until(EC.visibility_of_element_located(complete))
