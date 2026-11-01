import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import APP_PACKAGE

# ─────────────────────────────────────────────────────────────
# Inspector에서 찾은 값을 따옴표 안에 넣으세요.
#   상품 목록의 상품 하나를 클릭 → 오른쪽 Selected Element의 resource-id 복사
#   상세 화면의 "Add To Cart" 버튼을 클릭 → resource-id 복사
# 값이 비어 있으면 해당 테스트는 건너뜀(skip) 처리됩니다.
# ─────────────────────────────────────────────────────────────
PRODUCT_ID = ""      # 예: "com.saucelabs.mydemoapp.android:id/..."
ADD_TO_CART_ID = ""  # 예: "com.saucelabs.mydemoapp.android:id/..."


def test_app_launches(driver):
    """앱이 실행되고 현재 화면이 샘플 앱인지 확인"""
    assert driver.current_package == APP_PACKAGE


def test_open_product_detail(driver):
    """첫 번째 상품을 눌러 상세 화면의 장바구니 버튼이 보이는지 확인"""
    if not PRODUCT_ID or not ADD_TO_CART_ID:
        pytest.skip("Inspector에서 찾은 resource-id를 먼저 입력하세요")

    wait = WebDriverWait(driver, 10)  # 최대 10초 명시적 대기

    products = wait.until(
        EC.presence_of_all_elements_located((AppiumBy.ID, PRODUCT_ID))
    )
    assert len(products) > 0, "상품 목록이 비어 있음"
    products[0].click()

    add_button = wait.until(
        EC.visibility_of_element_located((AppiumBy.ID, ADD_TO_CART_ID))
    )
    assert add_button.is_displayed()
