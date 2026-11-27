from appium.webdriver.common.appiumby import AppiumBy

from locators import CARD_NUMBER_ID, FULL_NAME_ERROR_ID, LOGIN_BTN_ID
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from testdata import MSG_FULL_NAME_REQUIRED, PAYMENT, VALID_USER


def go_to_shipping(driver):
    """비로그인 상태로 결제를 진행하고, 나타난 로그인 화면에서 로그인까지 한다"""
    page = CheckoutPage(driver).add_first_product_and_checkout()
    LoginPage(driver).login(VALID_USER["username"], VALID_USER["password"])
    return page


def test_checkout_requires_login(driver):
    """비로그인 상태로 결제를 진행하면 로그인 후 배송지 입력 화면으로 이동하는지 확인"""
    page = go_to_shipping(driver)
    assert page.wait_for_shipping().is_displayed()


def test_checkout_when_logged_in(driver):
    """로그인 상태로 결제를 진행하면 로그인 화면 없이 배송지 입력 화면으로 이동하는지 확인"""
    login_page = LoginPage(driver).open_from_menu()
    login_page.login(VALID_USER["username"], VALID_USER["password"])
    login_page.wait_for_product_list()

    page = CheckoutPage(driver).add_first_product_and_checkout()
    assert page.wait_for_shipping().is_displayed()
    # 로그인 화면을 거치지 않았는지 확인
    assert not driver.find_elements(AppiumBy.ID, LOGIN_BTN_ID)


def test_shipping_required_fields(driver):
    """배송지를 비우고 To Payment를 누르면 필수값 에러가 보이는지 확인"""
    page = go_to_shipping(driver)
    page.wait_for_shipping()
    page.tap_to_payment()

    # 에러 TextView는 처음엔 invisible일 수 있으므로 visibility로 기다림
    assert page.error_text(FULL_NAME_ERROR_ID) == MSG_FULL_NAME_REQUIRED
    # 결제 정보 화면으로 넘어가지 않았는지도 확인
    assert not driver.find_elements(AppiumBy.ID, CARD_NUMBER_ID)


def test_shipping_to_payment(driver):
    """배송지를 입력하고 To Payment를 누르면 결제 정보 화면으로 이동하는지 확인"""
    page = go_to_shipping(driver)
    page.fill_shipping().tap_to_payment()
    assert page.wait_for_payment().is_displayed()


def test_checkout_complete(driver):
    """결제 정보를 입력하고 주문하면 Checkout Complete 화면이 보이는지 확인"""
    page = go_to_shipping(driver)
    page.fill_shipping().tap_to_payment().fill_payment().place_order()
    assert page.is_checkout_complete()


def test_payment_required_fields(driver):
    """카드 번호를 비우고 Review Order를 누르면 주문 확인 화면으로 넘어가지 않는지 확인"""
    page = go_to_shipping(driver)
    page.fill_shipping().tap_to_payment().wait_for_payment()
    page.fill_payment({**PAYMENT, "card_number": ""}).tap_review_order()

    # 앱은 에러 문구 없이 카드 번호 입력란 테두리만 빨갛게 표시함
    # → 주문 확인 화면으로 넘어가지 않고 결제 정보 화면에 남아 있는지로 검증
    assert not page.is_review_order_shown()
    assert page.wait_for_payment().is_displayed()
