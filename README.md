# mobile-qa-automation

![lint](https://github.com/ereemee/mobile-qa-automation/actions/workflows/lint.yml/badge.svg)

Python + pytest + Appium(UiAutomator2)으로 Sauce Labs 데모 앱(Android)의 주요 사용자 흐름을 Android 에뮬레이터에서 자동화 테스트하는 프로젝트입니다.

## 기술 스택
| 구분 | 사용 기술 |
| --- | --- |
| 언어 | Python 3.15.2 |
| 테스트 프레임워크 | pytest |
| 모바일 자동화 | Appium + UiAutomator2 driver, Appium-Python-Client |
| 대기 처리 | Selenium `WebDriverWait` + `expected_conditions` (명시적 대기) |
| 테스트 대상 | Sauce Labs My Demo App (`com.saucelabs.mydemoapp.android`) |
| 실행 환경 | Windows, PowerShell, Android Emulator (`emulator-5554`) |
| 코드 품질 / CI | ruff (lint·포맷 검사), GitHub Actions |

## 테스트 범위
| 테스트 | 검증 내용 |
| --- | --- |
| `test_app_launches` | 앱이 실행되고 현재 화면이 샘플 앱(`com.saucelabs.mydemoapp.android`)인지 확인 |
| `test_open_product_detail` | 첫 번째 상품을 눌러 상세 화면의 장바구니(Add To Cart) 버튼이 보이는지 확인 |
| `test_add_to_cart` | 상품을 장바구니에 담으면 장바구니 뱃지 숫자가 담기 전보다 1 늘어나는지 확인 |
| `test_login_success` | 메뉴 → Log In 화면에서 올바른 계정으로 로그인하면 상품 목록 화면으로 이동하는지 확인 |
| `test_login_empty_username` | 아이디 없이 Login을 누르면 "Username is required" 에러 메시지가 보이는지 확인 |
| `test_checkout_requires_login` | 비로그인 상태로 결제를 진행하면 로그인 후 배송지 입력 화면으로 이동하는지 확인 |
| `test_login_locked_account` | 잠긴 계정으로 로그인하면 "Sorry this user has been locked out." 에러 메시지가 보이는지 확인 |
| `test_login_state_resets_after_restart` | 로그인 후 앱을 재시작하면 로그아웃 상태(메뉴에 Log In 표시)로 돌아오는지 확인 |
| `test_shipping_to_payment` | 로그인 후 배송지를 입력하고 To Payment를 누르면 결제 정보(카드 번호 입력) 화면으로 이동하는지 확인 |
| `test_checkout_complete` | 배송지·결제 정보를 입력하고 Review Order → Place Order를 누르면 Checkout Complete 화면이 보이는지 확인 |

모든 테스트는 `conftest.py`의 `driver` fixture를 사용합니다. 테스트마다 앱을 종료(`terminate_app`)했다가 다시 실행(`activate_app`)하고, 앱이 화면 맨 앞에 올 때까지 기다린 뒤 시작합니다. 그래서 각 테스트가 항상 첫 화면(상품 목록)에서 독립적으로 실행됩니다.

테스트가 실패하면 `conftest.py`의 `pytest_runtest_makereport` hook이 그 순간의 에뮬레이터 화면을 캡처해 `screenshots/테스트이름_날짜시간.png`로 저장합니다. (`screenshots/`는 `.gitignore`로 커밋에서 제외)

## 사전 준비
1. **Android SDK / 에뮬레이터**: Android Studio에서 에뮬레이터를 만들고 실행합니다. `adb devices`에서 `emulator-5554`가 보여야 합니다.
2. **테스트 앱 설치**: 에뮬레이터에 Sauce Labs My Demo App(Android)을 설치합니다.
3. **Node.js** 설치
4. **Appium 서버와 드라이버 설치**
   ```powershell
   npm install -g appium
   appium driver install uiautomator2
   ```
5. **Python 패키지 설치**
   ```powershell
   python -m pip install -r requirements.txt
   ```

## 실행 방법
```powershell
# 1) Appium 서버 실행 (별도 PowerShell 창, 기본 주소 http://127.0.0.1:4723)
appium

# 2) 테스트 실행 (프로젝트 폴더에서)
cd C:\Users\hyeri\projects\mobile-qa-automation
python -m pytest

# 특정 테스트만 실행
python -m pytest tests/test_app.py::test_add_to_cart
```
> `pytest.ini`에 `testpaths = tests`, `addopts = -v`가 설정되어 있어서 `tests/` 폴더의 테스트가 상세 모드로 실행됩니다.
> Appium Inspector 세션이 열려 있으면 테스트 세션과 충돌하므로, 실행 전에 Inspector 세션을 닫아 주세요.

## 코드 품질 (lint / CI)
`main` 브랜치에 push하거나 Pull Request를 만들면 GitHub Actions(`.github/workflows/lint.yml`)가 ruff로 lint와 포맷을 자동으로 검사합니다. Appium 테스트는 에뮬레이터가 필요하므로 CI에서는 정적 검사만 실행합니다.

```powershell
# 개발용 도구 설치
python -m pip install -r requirements-dev.txt

# 로컬에서 검사 (CI와 같은 명령)
python -m ruff check .
python -m ruff format --check .

# 자동 수정
python -m ruff format .
python -m ruff check --fix .
```
> 검사 규칙은 `ruff.toml`에 설정되어 있습니다. (`E`, `F`, `I` 규칙, 한 줄 최대 100자)

### 커밋 전 자동 검사 (git hook)
```powershell
git config core.hooksPath .githooks   # 최초 1회
```
`git commit`을 하면 `.githooks/pre-commit`이 ruff check와 ruff format --check를 먼저 실행하고, 실패하면 커밋이 멈춥니다.
   
## 폴더 구조
```
mobile-qa-automation/
├── .github/
│   └── workflows/
│       └── lint.yml   # GitHub Actions: push·PR 시 ruff lint·포맷 검사
├── .githooks/
│   ├── pre-commit # 커밋 전 ruff 검사 hook
├── conftest.py        # driver fixture (capability 설정, 앱 재시작·대기, 세션 종료), 실패 시 스크린샷 hook
├── pytest.ini         # pytest 설정 (testpaths, pythonpath, -v)
├── ruff.toml          # ruff 검사 규칙 설정
├── requirements.txt   # Python 의존성 (버전 고정)
├── requirements-dev.txt # 개발용 도구 (ruff, 버전 고정)
├── tests/
│   ├── test_app.py      # 앱 실행 / 상품 상세 / 장바구니 테스트
│   ├── test_login.py    # 로그인 성공 / 실패 / 잠금 계정 / 재시작 테스트
│   └── test_checkout.py # 결제 흐름 테스트 (로그인 → 배송지 → 결제 정보 → 주문 완료)
├── docs/
│   └── images/        # README용 실행 결과 이미지
├── screenshots/       # 테스트 실패 시 자동 생성 (git 제외)
├── TODO.md            # 앞으로 할 일
└── README.md
```

## 실행 결과
![pytest 실행 결과](docs/images/pytest-result.png)

## 트러블슈팅
### 1. PowerShell에서 `pytest` 명령을 인식하지 못함
- **문제**: PowerShell에서 `pytest`를 입력하면 명령을 인식하지 못함
- **원인**: pytest 실행 파일이 있는 Scripts 폴더가 PATH에 등록되어 있지 않음
- **해결**: `python -m pytest`로 실행해서 현재 Python에 설치된 pytest 모듈을 직접 호출

### 2. 상품 목록 요소를 찾지 못해 `TimeoutException`
- **문제**: 상품 목록 locator로 요소를 기다리다가 타임아웃
- **원인**: 추측한 resource-id가 실제 값과 달랐고, 이전 테스트가 끝난 화면(상세 화면 등)에서 다음 테스트가 시작됨
- **해결**: Appium Inspector와 page source로 실제 resource-id(`productIV`)를 확인해서 적용. `conftest.py`에서 `terminate_app` 후 `activate_app`을 호출해 매번 첫 화면에서 시작하도록 수정

### 3. 앱 실행 직후 검사에서 현재 화면이 홈 화면(launcher)으로 나옴
- **문제**: `test_app_launches`에서 `current_package`가 `com.google.android.apps.nexuslauncher`로 나와 실패
- **원인**: `activate_app`이 앱이 화면에 완전히 뜨기 전에 끝나서, 검사하는 순간에는 아직 홈 화면이었음
- **해결**: `conftest.py`에서 `current_package`가 샘플 앱이 될 때까지 `WebDriverWait`로 최대 15초 기다리도록 수정

### 4. 장바구니 뱃지 값이 비어 있어 `ValueError: invalid literal for int() with base 10: ''`
- **문제**: 담기 버튼 클릭 직후 뱃지 text를 `int()`로 변환하다 실패
- **원인**: 뱃지 숫자가 아직 갱신되기 전이라 text가 빈 문자열
- **해결**: 담기 전 개수를 먼저 저장하고, 뱃지 숫자가 `담기 전 + 1`이 될 때까지 `WebDriverWait`로 기다린 뒤 검증 (빈 값은 0으로 처리)

### 5. Appium Inspector 사용 시 주의점
- **문제**: Inspector 스크린샷을 클릭해도 앱 화면이 넘어가지 않고, Inspector를 켠 채로 pytest를 실행하면 세션이 꼬임
- **원인**: 스크린샷 클릭은 앱을 조작하지 않고 요소만 선택함. Inspector도 하나의 Appium 세션을 사용함
- **해결**: 화면 이동은 에뮬레이터에서 직접 하고, pytest 실행 전에는 Inspector 세션을 닫음

## 앞으로 할 일
[TODO.md](TODO.md) 참고 — 결제(Checkout) 흐름 테스트, 로그인 실패 케이스 확장, Page Object Model 리팩터링, locator·테스트 데이터 분리, pytest-html 리포트, 클라우드 디바이스 팜 연동 예정
