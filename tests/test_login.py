from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from conftest import APP_PACKAGE
from locators import (
    LOGIN_BTN_ID,
    MENU_ID,
    NAME_ERROR_ID,
    PASSWORD_ERROR_ID,
    PASSWORD_ID,
    PRODUCT_ID,
    USERNAME_ID,
)


def open_login_screen(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, MENU_ID))).click()
    wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Log In")')
        )
    ).click()
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
    """아이디 없이 로그인하면 'Username is required' 에러 메시지가 보이는지 확인"""
    wait = open_login_screen(driver)
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, LOGIN_BTN_ID))).click()
    # nameErrorTV는 처음부터 있지만 invisible → visibility로 기다림
    error = wait.until(EC.visibility_of_element_located((AppiumBy.ID, NAME_ERROR_ID)))
    assert error.text == "Username is required"


def login(driver, wait, username, password):
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, USERNAME_ID))).send_keys(username)
    driver.find_element(AppiumBy.ID, PASSWORD_ID).send_keys(password)
    driver.find_element(AppiumBy.ID, LOGIN_BTN_ID).click()


def test_login_locked_account(driver):
    """잠긴 계정으로 로그인하면 잠금 에러 메시지가 보이는지 확인"""
    wait = open_login_screen(driver)
    login(driver, wait, "alice@example.com", "10203040")
    error = wait.until(EC.visibility_of_element_located((AppiumBy.ID, PASSWORD_ERROR_ID)))
    assert error.text == "Sorry this user has been locked out."


def test_login_state_resets_after_restart(driver):
    """로그인 후 앱을 재시작하면 로그아웃 상태(메뉴에 Log In)로 돌아오는지 확인"""
    wait = open_login_screen(driver)
    login(driver, wait, "bod@example.com", "10203040")
    wait.until(EC.presence_of_all_elements_located((AppiumBy.ID, PRODUCT_ID)))

    driver.terminate_app(APP_PACKAGE)
    driver.activate_app(APP_PACKAGE)

    wait.until(EC.element_to_be_clickable((AppiumBy.ID, MENU_ID))).click()
    log_in = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Log In")')
    assert wait.until(EC.visibility_of_element_located(log_in))
