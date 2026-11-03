# TODO

## 완료
- [x] Appium + UiAutomator2 환경 구성, driver fixture (conftest.py)
- [x] 앱 실행 확인 테스트
- [x] 상품 상세 화면 진입 테스트
- [x] 장바구니 담기 테스트 (담기 전 개수 + 1 검증)
- [x] 매 테스트마다 앱 재시작(terminate_app → activate_app) 및 앱이 앞에 올 때까지 대기
- [x] requirements.txt 버전 고정
- [x] README 작성 (실행 방법·트러블슈팅)

## 다음 할 일
- [ ] 로그인 테스트 (성공 / 실패 케이스)
- [ ] 장바구니 → 결제(Checkout) 흐름 테스트
- [ ] Page Object Model 구조로 리팩터링 (pages/ 폴더)
- [ ] locator·테스트 데이터 분리
- [ ] 실패 시 스크린샷 자동 저장 (conftest hook)
- [ ] pytest-html 리포트 생성
- [ ] GitHub Actions로 lint(ruff) 자동 검사
- [ ] AWS Device Farm 등 클라우드 디바이스 팜 연동 검토
