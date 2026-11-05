from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import APP_PACKAGE

# Appium Inspector / page source로 확인한 resource-id
PRODUCT_ID = "com.saucelabs.mydemoapp.android:id/productIV"
ADD_TO_CART_ID = "com.saucelabs.mydemoapp.android:id/cartBt"
CART_BADGE_ID = "com.saucelabs.mydemoapp.android:id/cartTV"


def get_cart_count(driver):
    """장바구니 뱃지 숫자를 읽는다. 뱃지가 없거나 text가 비어 있으면 0"""
    badges = driver.find_elements(AppiumBy.ID, CART_BADGE_ID)
    if not badges or not badges[0].text.strip():
        return 0
    return int(badges[0].text)


def test_app_launches(driver):
    """앱이 실행되고 현재 화면이 샘플 앱인지 확인"""
    assert driver.current_package == APP_PACKAGE


def test_open_product_detail(driver):
    """첫 번째 상품을 눌러 상세 화면의 장바구니 버튼이 보이는지 확인"""
    wait = WebDriverWait(driver, 10)  # 최대 10초 명시적 대기

    products = wait.until(EC.presence_of_all_elements_located((AppiumBy.ID, PRODUCT_ID)))
    assert len(products) > 0, "상품 목록이 비어 있음"
    products[0].click()

    add_button = wait.until(EC.visibility_of_element_located((AppiumBy.ID, ADD_TO_CART_ID)))
    assert add_button.is_displayed()


def test_add_to_cart(driver):
    """상품을 장바구니에 담으면 뱃지 숫자가 1 늘어나는지 확인"""
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((AppiumBy.ID, PRODUCT_ID)))[0].click()
    add_button = wait.until(EC.element_to_be_clickable((AppiumBy.ID, ADD_TO_CART_ID)))

    before = get_cart_count(driver)
    add_button.click()
    wait.until(lambda d: get_cart_count(d) == before + 1)  # int('') ValueError 방지
    assert get_cart_count(driver) == before + 1
