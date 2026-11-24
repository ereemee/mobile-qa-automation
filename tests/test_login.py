from conftest import restart_app
from locators import NAME_ERROR_ID, PASSWORD_ERROR_ID
from pages.login_page import LoginPage
from testdata import LOCKED_USER, MSG_LOCKED_OUT, MSG_USERNAME_REQUIRED, VALID_USER


def test_login_success(driver):
    """올바른 계정으로 로그인하면 상품 목록 화면으로 이동하는지 확인"""
    page = LoginPage(driver).open_from_menu()
    page.login(VALID_USER["username"], VALID_USER["password"])
    assert page.wait_for_product_list()


def test_login_empty_username(driver):
    """아이디 없이 로그인하면 'Username is required' 에러 메시지가 보이는지 확인"""
    page = LoginPage(driver).open_from_menu()
    page.tap_login()
    assert page.error_text(NAME_ERROR_ID) == MSG_USERNAME_REQUIRED


def test_login_locked_account(driver):
    """잠긴 계정으로 로그인하면 잠금 에러 메시지가 보이는지 확인"""
    page = LoginPage(driver).open_from_menu()
    page.login(LOCKED_USER["username"], LOCKED_USER["password"])
    assert page.error_text(PASSWORD_ERROR_ID) == MSG_LOCKED_OUT


def test_login_state_resets_after_restart(driver):
    """로그인 후 앱을 재시작하면 로그아웃 상태(메뉴에 Log In)로 돌아오는지 확인"""
    page = LoginPage(driver).open_from_menu()
    page.login(VALID_USER["username"], VALID_USER["password"])
    page.wait_for_product_list()
    restart_app(driver)  # 재시작 후 첫 화면이 뜰 때까지 기다림
    assert page.is_log_in_menu_shown()
