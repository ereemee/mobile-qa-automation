"""
결제 흐름 Page Object.
상품 담기 → 장바구니 → 배송지 → 결제 정보 → 주문 완료까지를 한 곳에서 관리한다.
"""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
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
    FULL_NAME_ID,
    PROCEED_ID,
    PRODUCT_ID,
    TO_PAYMENT_ID,
    ZIP_ID,
)
from testdata import PAYMENT, SHIPPING

PLACE_ORDER = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Place Order")')
CHECKOUT_COMPLETE = (
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().textContains("Checkout Complete")',
)


class CheckoutPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def add_first_product_and_checkout(self):
        """첫 상품 담기 → 장바구니 → Proceed To Checkout"""
        self.wait.until(EC.presence_of_all_elements_located((AppiumBy.ID, PRODUCT_ID)))[0].click()
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, ADD_TO_CART_ID))).click()
        self.wait.until(EC.text_to_be_present_in_element((AppiumBy.ID, CART_BADGE_ID), "1"))
        self.driver.find_element(AppiumBy.ID, CART_ICON_ID).click()
        self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, CART_LIST_ID)))
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, PROCEED_ID))).click()
        return self

    def scroll_to_text(self, text):
        """키보드를 내리고, 화면을 스크롤해서 text 요소를 돌려준다"""
        if self.driver.is_keyboard_shown():
            self.driver.hide_keyboard()
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            "new UiScrollable(new UiSelector().scrollable(true))"
            f'.scrollIntoView(new UiSelector().text("{text}"))',
        )

    def wait_for_shipping(self):
        """배송지 입력 화면(Full Name 입력란)이 보일 때까지 기다린다"""
        return self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, FULL_NAME_ID)))

    def fill_shipping(self, shipping=SHIPPING):
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, FULL_NAME_ID))).send_keys(
            shipping["full_name"]
        )
        self.driver.find_element(AppiumBy.ID, ADDRESS1_ID).send_keys(shipping["address1"])
        self.driver.find_element(AppiumBy.ID, CITY_ID).send_keys(shipping["city"])
        self.driver.find_element(AppiumBy.ID, ZIP_ID).send_keys(shipping["zip"])
        self.driver.find_element(AppiumBy.ID, COUNTRY_ID).send_keys(shipping["country"])
        return self

    def tap_to_payment(self):
        self.scroll_to_text("To Payment")
        self.driver.find_element(AppiumBy.ID, TO_PAYMENT_ID).click()
        return self

    def wait_for_payment(self):
        return self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, CARD_NUMBER_ID)))

    def fill_payment(self, payment=PAYMENT):
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, CARD_NAME_ID))).send_keys(
            payment["name"]
        )
        self.driver.find_element(AppiumBy.ID, CARD_NUMBER_ID).send_keys(payment["card_number"])
        self.driver.find_element(AppiumBy.ID, EXPIRATION_ID).send_keys(payment["expiration"])
        self.driver.find_element(AppiumBy.ID, CVV_ID).send_keys(payment["cvv"])
        return self

    def tap_review_order(self):
        """Review Order 버튼만 누른다 (필수값 검증용)"""
        self.scroll_to_text("Review Order").click()
        return self

    def place_order(self):
        self.scroll_to_text("Review Order").click()
        self.wait.until(EC.element_to_be_clickable(PLACE_ORDER)).click()

    def error_text(self, error_id):
        """에러 TextView가 보일 때까지 기다렸다가 text를 돌려준다 (처음엔 invisible)"""
        return self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, error_id))).text

    def is_checkout_complete(self):
        return self.wait.until(EC.visibility_of_element_located(CHECKOUT_COMPLETE)).is_displayed()

    def is_review_order_shown(self, timeout=3):
        """Place Order 버튼(주문 확인 화면)이 timeout초 안에 나타나면 True"""
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(PLACE_ORDER))
            return True
        except TimeoutException:
            return False
