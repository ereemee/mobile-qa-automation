"""
pytest 공통 설정 파일.
여기서 만든 driver fixture를 모든 테스트가 함께 사용한다.
(Selenium의 setUp / tearDown 역할)
"""

import base64
import os
from datetime import datetime

import pytest
import pytest_html
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from locators import PRODUCT_ID

APPIUM_SERVER = os.getenv("APPIUM_SERVER", "http://127.0.0.1:4723")
DEVICE_NAME = os.getenv("DEVICE_NAME", "emulator-5554")
APP_PACKAGE = "com.saucelabs.mydemoapp.android"


def restart_app(drv):
    """앱을 껐다가 다시 실행하고, 첫 화면(상품 목록)이 나타날 때까지 기다린다"""
    drv.terminate_app(APP_PACKAGE)
    drv.activate_app(APP_PACKAGE)
    # activate_app은 앱이 화면에 뜨기 전에 끝날 수 있으므로,
    # 샘플 앱이 실제로 맨 앞 화면이 될 때까지 최대 15초 대기
    WebDriverWait(drv, 15).until(
        lambda d: d.current_package == APP_PACKAGE,
        message=f"{APP_PACKAGE} 앱이 15초 안에 화면 맨 앞으로 오지 않음",
    )
    # 상품 목록이 늦게 그려지거나, 느린 에뮬레이터에서 AccessibilityNodeInfo 타임아웃
    # (WebDriverException)이 잠깐 나도 바로 실패하지 않고 최대 30초 다시 시도
    WebDriverWait(drv, 30, ignored_exceptions=[WebDriverException]).until(
        EC.presence_of_all_elements_located((AppiumBy.ID, PRODUCT_ID)),
        message="상품 목록이 30초 안에 나타나지 않음",
    )


@pytest.fixture
def driver():
    # Inspector에 넣었던 capability와 같은 값
    options = UiAutomator2Options()
    options.device_name = DEVICE_NAME
    options.no_reset = True  # 테스트 때마다 앱 데이터를 지우지 않음
    # 일부 에뮬레이터에서 Hidden API 설정 변경이 막혀 세션 생성이 실패하는 문제 우회
    options.set_capability("appium:ignoreHiddenApiPolicyError", True)
    # 느린 에뮬레이터를 위해 대기 시간 늘리기 (단위: ms)
    options.set_capability("appium:adbExecTimeout", 60000)
    options.set_capability("appium:uiautomator2ServerInstallTimeout", 120000)
    options.set_capability("appium:uiautomator2ServerLaunchTimeout", 120000)

    drv = webdriver.Remote(APPIUM_SERVER, options=options)
    # 이전 테스트가 끝난 화면(상세·장바구니 등)이 남지 않도록 앱을 재시작
    restart_app(drv)
    yield drv  # 여기서 테스트가 실행됨

    drv.quit()  # 테스트가 끝나면 세션 종료


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield  # 테스트 결과(report)를 받음
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            png_b64 = drv.get_screenshot_as_base64()
            # 1) 기존처럼 screenshots/ 폴더에 파일로 저장
            os.makedirs("screenshots", exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f"screenshots/{item.name}_{ts}.png", "wb") as f:
                f.write(base64.b64decode(png_b64))
            # 2) pytest-html 리포트의 해당 테스트 행에 같은 화면을 첨부
            extras = getattr(report, "extras", [])
            extras.append(pytest_html.extras.png(png_b64, name="실패 화면"))
            report.extras = extras
    return report
