"""
pytest 공통 설정 파일.
여기서 만든 driver fixture를 모든 테스트가 함께 사용한다.
(Selenium의 setUp / tearDown 역할)
"""
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

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
    drv.activate_app(APP_PACKAGE)  # 샘플 앱 실행 (이미 켜져 있으면 앞으로 가져옴)

    yield drv  # 여기서 테스트가 실행됨

    drv.quit()  # 테스트가 끝나면 세션 종료
