"""
pytest 공통 설정 파일.
여기서 만든 driver fixture를 모든 테스트가 함께 사용한다.
(Selenium의 setUp / tearDown 역할)
"""
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait
import os
from datetime import datetime

APPIUM_SERVER = "http://127.0.0.1:4723"
APP_PACKAGE = "com.saucelabs.mydemoapp.android"


@pytest.fixture
def driver():
    # Inspector에 넣었던 capability와 같은 값
    options = UiAutomator2Options()
    options.device_name = "emulator-5554"
    options.no_reset = True  # 테스트 때마다 앱 데이터를 지우지 않음
    # 일부 에뮬레이터에서 Hidden API 설정 변경이 막혀 세션 생성이 실패하는 문제 우회
    options.set_capability("appium:ignoreHiddenApiPolicyError", True)
    # 느린 에뮬레이터를 위해 대기 시간 늘리기 (단위: ms)
    options.set_capability("appium:adbExecTimeout", 60000)
    options.set_capability("appium:uiautomator2ServerInstallTimeout", 120000)
    options.set_capability("appium:uiautomator2ServerLaunchTimeout", 120000)

    drv = webdriver.Remote(APPIUM_SERVER, options=options)

    # 이전 테스트가 끝난 화면(상세·장바구니 등)이 남지 않도록 앱을 껐다가 다시 실행
    drv.terminate_app(APP_PACKAGE)
    drv.activate_app(APP_PACKAGE)
    # activate_app은 앱이 화면에 뜨기 전에 끝날 수 있으므로,
    # 샘플 앱이 실제로 맨 앞 화면이 될 때까지 최대 15초 대기
    WebDriverWait(drv, 15).until(
        lambda d: d.current_package == APP_PACKAGE,
        message=f"{APP_PACKAGE} 앱이 15초 안에 화면 맨 앞으로 오지 않음",
    )
    yield drv  # 여기서 테스트가 실행됨

    drv.quit()  # 테스트가 끝나면 세션 종료


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield  # 테스트 결과(report)를 받음
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            os.makedirs("screenshots", exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            drv.save_screenshot(f"screenshots/{item.name}_{ts}.png")
    return report