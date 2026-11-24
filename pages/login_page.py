"""
로그인 화면 Page Object.
메뉴 → Log In 이동, 아이디/비밀번호 입력, 에러 메시지 읽기를 한 곳에서 관리한다.
"""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators import LOGIN_BTN_ID, MENU_ID, PASSWORD_ID, PRODUCT_ID, USERNAME_ID

LOG_IN_MENU = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Log In")')


class LoginPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open_menu(self):
        """왼쪽 위 메뉴를 연다"""
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, MENU_ID))).click()
        return self

    def open_from_menu(self):
        """메뉴 → Log In을 눌러 로그인 화면으로 이동한다"""
        self.open_menu()
        self.wait.until(EC.element_to_be_clickable(LOG_IN_MENU)).click()
        return self

    def login(self, username, password):
        """현재 로그인 화면에서 아이디·비밀번호를 입력하고 Login을 누른다"""
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, USERNAME_ID))).send_keys(username)
        self.driver.find_element(AppiumBy.ID, PASSWORD_ID).send_keys(password)
        self.driver.find_element(AppiumBy.ID, LOGIN_BTN_ID).click()

    def tap_login(self):
        """아무것도 입력하지 않고 Login 버튼만 누른다"""
        self.wait.until(EC.element_to_be_clickable((AppiumBy.ID, LOGIN_BTN_ID))).click()

    def error_text(self, error_id):
        """에러 TextView가 보일 때까지 기다렸다가 text를 돌려준다 (처음엔 invisible)"""
        return self.wait.until(EC.visibility_of_element_located((AppiumBy.ID, error_id))).text

    def wait_for_product_list(self):
        """로그인 성공 후 상품 목록이 나타날 때까지 기다린다"""
        return self.wait.until(EC.presence_of_all_elements_located((AppiumBy.ID, PRODUCT_ID)))

    def is_log_in_menu_shown(self):
        """메뉴를 열었을 때 Log In 항목이 보이면 True (로그아웃 상태)"""
        self.open_menu()
        return self.wait.until(EC.visibility_of_element_located(LOG_IN_MENU)).is_displayed()
