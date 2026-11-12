# TODO

## 완료
- [x] Appium + UiAutomator2 환경 구성, driver fixture (conftest.py)
- [x] 앱 실행 확인 테스트
- [x] 상품 상세 화면 진입 테스트
- [x] 장바구니 담기 테스트 (담기 전 개수 + 1 검증)
- [x] 매 테스트마다 앱 재시작(terminate_app → activate_app) 및 앱이 앞에 올 때까지 대기
- [x] requirements.txt 버전 고정
- [x] README 작성 (실행 방법·트러블슈팅)
- [x] 실패 시 스크린샷 자동 저장 (conftest hook)
- [x] 로그인 테스트 (성공 케이스)
- [x] 로그인 실패(빈 아이디) 에러 메시지 검증
- [x] GitHub Actions로 lint(ruff) 자동 검사
- [x] lint 오류 수정 (중복 테스트 함수 제거)
- [x] 비로그인 결제 진입 → 로그인 → 배송지 화면 이동 테스트
- [x] 잠금 계정 로그인 실패 케이스 추가
- [x] 로그인 상태 초기화 방법 정리 (terminate_app 후 Log In 상태로 돌아오는지 테스트로 확인)
- [x] 결제 2단계: 배송지 입력 → To Payment → 결제 정보 화면 (go_to_shipping 헬퍼 분리)
- [x] 결제 3단계: 결제 정보 입력 → 주문 확인 → Checkout Complete 검증
- [x] ruff format 오류 수정 (test_checkout.py), 배송지 입력 fill_shipping 헬퍼 분리

## 다음 할 일
- [ ] 배송지 필수값 미입력 에러 메시지 검증
- [ ] 로그인 상태로 결제 진입 시 로그인 화면 없이 배송지로 이동하는지 검증
- [ ] 공통 locator(PKG, 로그인 id 등)를 한 곳으로 모으기 (test_login.py·test_checkout.py 중복)
- [ ] Page Object Model 구조로 리팩터링 (pages/ 폴더)
- [ ] locator·테스트 데이터 분리
- [ ] pytest-html 리포트 생성
- [ ] 실패 스크린샷을 pytest-html 리포트에 첨부
- [ ] AWS Device Farm 등 클라우드 디바이스 팜 연동 검토
- [ ] 결제 정보 필수값 미입력(카드 번호 등) 에러 메시지 검증
- [ ] go_to_shipping·fill_shipping 헬퍼를 pages/ 로 옮기기 (POM 리팩터링 첫 단계)
- [ ] 커밋 전 ruff 자동 실행 (pre-commit hook)