# tests/test_login.py
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PKG = "com.saucelabs.mydemoapp.android:id/"
MENU_ID = PKG + "menuIV"     
USERNAME_ID = PKG + "nameET"
PASSWORD_ID = PKG + "passwordET"  
LOGIN_BTN_ID = PKG + "loginBtn"
PRODUCT_ID = PKG + "productIV"

def open_login_screen(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, MENU_ID))).click()
    wait.until(EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Log In")')
    )).click()
    return wait

def test_login_success(driver):
    """올바른 계정으로 로그인하면 상품 목록 화면으로 이동하는지 확인"""
    wait = open_login_screen(driver)
    # 로그인 화면이 뜰 때까지 아이디 입력란을 기다렸다가 입력
    username = wait.until(EC.element_to_be_clickable((AppiumBy.ID, USERNAME_ID)))
    username.send_keys("bod@example.com")
    driver.find_element(AppiumBy.ID, PASSWORD_ID).send_keys("10203040")
    driver.find_element(AppiumBy.ID, LOGIN_BTN_ID).click()
    # 로그인 성공 → 상품 목록 화면으로 이동
    assert wait.until(EC.presence_of_all_elements_located((AppiumBy.ID, PRODUCT_ID)))

        
def test_login_empty_username(driver):
    """아이디 없이 로그인하면 에러 메시지가 보이는지 확인"""
    wait = open_login_screen(driver)
    driver.find_element(AppiumBy.ID, LOGIN_BTN_ID).click()
    # TODO: Inspector에서 확인한 에러 메시지 ID/text로 검증