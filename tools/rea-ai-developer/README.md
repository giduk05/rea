# REA AI Developer — 첫 번째 Gemini 연동 실험

**기존 REA main은 수정하지 않습니다.** 이 실험은 별도 브랜치와 tools/rea-ai-developer 폴더만 사용합니다.

## 지금 자동으로 검증하는 것

1. 소스에서 REA 설치/빌드.
2. 저장소에서 직접 작성한 fixture/index.js와 fixture/passage.js를 **실제 REA**로 분석.
3. REA가 두 모듈과 정상 해석된 import 관계를 찾았는지 검사.
4. 오프라인 지문 정리기 demo.html을 index.html로 복사하고 문법 검사.
5. evidence.json, rea-summary.json, report.json, index.html을 GitHub Actions artifact로 보관.

오프라인 데모는 AI 생성물이 **아닙니다**. API 호출은 오프라인 잡에서 0회입니다.

## Gemini를 이용한 실제 코드 생성 (아직 비활성)

Gemini 실험은 별도의 workflow_dispatch 작업으로 수동 시작합니다. 해당 워크플로가 기본 브랜치에 등록되어야 Run workflow가 나타납니다. GitHub 저장소 Settings → Secrets and variables → Actions → New repository secret에서 GEMINI_API_KEY 등록.

실행 전에 반드시 https://aistudio.google.com/ 의 Projects에서 키가 속한 프로젝트 Billing Tier가 **Free**인지 확인하세요. Run workflow에서 run_gemini=true, free_tier_acknowledgement=I_VERIFIED_FREE_TIER 입력. 코드는 gemini-3.6-flash만 허용합니다. Gemini 공식 API 한 번만 호출하며 자동 재시도, 유료 fallback, GLM 호출은 없습니다.

**주의:** 코드의 모델 제한과 승인 문자열은 프로젝트가 실제 무료 계정임을 자동 검증하지 못합니다. 유료 프로젝트의 키를 사용하면 요금이 발생할 수 있으니 키를 공유하지 마세요.

Gemini는 REA 분석 요약을 받아 **인터넷 없이 실행하는 영어 지문 정리용 단일 HTML 앱**을 생성합니다. HTML/JavaScript 구문 검사를 통과한 결과만 artifact로 저장하고, 코드를 자동 실행하거나 GitHub에 자동 커밋하지 않습니다. 생성 코드의 기능/안전성은 사람이 추가 확인해야 합니다.

Gemini 공식 문서: https://ai.google.dev/api/generate-content
무료/과금 정책: https://ai.google.dev/gemini-api/docs/billing

## 다음 단계

REA+Gemini 실사용 1회 성공 후 같은 무과금 게이트로 GLM을 추가합니다. 대형 앱 역공학이나 상용 앱 복제를 현재 지원한다고 주장하지 않습니다.
