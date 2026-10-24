# 변경 내역

Research Loop는 버전이 하나입니다. 웹사이트, MCP 서버, ChatGPT·Claude 안의 패널, 이 플러그인 패키지가 같은 번호를 씁니다. 새 버전은 맨 위에 `## x.y.z` 항목으로 적습니다. 항목의 첫 문단은 플러그인 디렉터리에 올라가는 release note이므로 영어 한 문단으로 쓰고, 그 아래에 사람이 읽을 내용을 한국어로 적습니다. 릴리스 명령이 제목에 날짜를 붙입니다.

## 0.70.0 — 2026-10-23

Slides no longer cut words, and PPTX export no longer refuses. Text, lists, tables, captions and titles are measured with glyph widths taken from the fonts, set smaller down to a floor, and past it drawn whole and marked. A checks list in the studio names each place to fix, with one-click fixes: grow the box, or continue on the next slide. PPTX files use Pretendard with Korean attributes, soft wraps, point line spacing and tables shaped like the screen, and the studio says what went in overflowing.

- 슬라이드의 글이 상자 경계에서 잘리지 않습니다. 글·목록·도형·표·캡션·제목이 정한 크기로 들어가지 않으면 하한(본문·표 12pt, 제목 24pt)까지 줄이고, 그래도 넘치면 상자 밖까지 다 보이게 그린 뒤 '넘침'으로 표시합니다.
- 글자 폭을 어림하지 않고 글꼴 파일에서 잰 표로 잽니다. 줄은 화면 글꼴(Pretendard)로 나누고, 크기와 들어감은 PowerPoint·Google Slides가 대신 쓸 수 있는 글꼴까지 가장 넓은 폭으로 판정해, 어느 글꼴로 열어도 줄이 늘지 않습니다. 한글 줄은 전보다 상자를 더 채웁니다.
- 표는 내용에 맞춰 열 너비를 나누고 숫자 열은 오른쪽으로 정렬합니다. 그림 캡션은 필요한 만큼 여러 줄이 되고 그만큼 그림이 작아집니다(캡션이 상자의 40%를 넘으면 표시). 차트 항목 이름이 길면 16px까지 줄이고 두 줄로 씁니다.
- 편집 화면 머리의 '점검 N'에서 고칠 곳과 다듬을 곳을 한 번에 보고, 줄을 누르면 그 슬라이드의 그 상자로 갑니다. 고칠 곳이 있는 슬라이드에는 점이, 상자에는 주의 테두리와 꼬리표가 붙습니다. 상자를 고르면 '상자 키우기'나 '다음 슬라이드로 잇기'로 바로 고칩니다. 잇기는 들어가는 만큼 남기고 나머지를 바로 뒤 새 슬라이드로 옮깁니다(목록은 항목, 표는 행, 글은 문단이나 문장 단위).
- PPTX 내보내기는 맞춤 때문에 거부하지 않습니다. 글꼴은 Pretendard(세리프 슬라이드는 MaruBuri)이고, 한글 문자 집합과 ko-KR 언어를 적으며, 강제 줄바꿈 없이 문단만 나누고, 줄 간격은 화면과 같은 pt 값입니다. 표의 열 너비·선·정렬도 화면과 같습니다. 내보낸 뒤 머리 아래 띠가 넘친 곳과 읽지 못한 그림을 슬라이드 링크와 함께 알립니다.
- 음수 막대의 값이 아래 항목 이름과 겹치던 문제와, 고치는 중인 슬라이드의 썸네일이 바로 바뀌지 않던 문제를 고쳤습니다.
- 80장 발표를 그리는 시간이 8.19ms에서 3.27ms로 줄었습니다.
- 배포: 마이그레이션과 저장 형식 변경은 없습니다. 사이트와 MCP 함수(패널)를 다시 올립니다.

## 0.69.0 — 2026-10-20

Notes an AI writes as an A-to-Z explanation can now be bound like a book: a cover note's fields.series orders 2–40 notes. The cover lists the parts before its body; each part shows its series and place under its title, unfolds the contents, and ends with the previous and next parts. People reorder or take parts out on the cover, and the notes stay. The writing guide (42) tells AIs to write such explanations as a series, and the MCP server refuses a series that breaks a rule, naming it.

- AI에게 어떤 개념을 처음부터 끝까지, 단계별로 설명해 달라고 하면 보통 노트 여러 편으로 나눠 씁니다. 이제 이 노트들을 책처럼 시리즈로 묶습니다. 표지 노트 하나가 2–40편의 순서를 가지고, 데이터베이스 변경은 없습니다.
- 표지에서는 본문 앞의 목차에서 편마다 번호, 제목, 한 줄 설명을 보고 '1편부터 읽기'로 시작합니다. 각 편에는 제목 아래에 시리즈 이름과 '2/3편', 그 자리에서 펼치는 목차가 있고, 본문 끝에 이전 편과 다음 편이 있습니다. 첫 편의 이전과 마지막 편의 다음은 표지로 갑니다. 편을 넘겨도 읽기 창의 위치와 전체 화면은 그대로입니다.
- 표지의 '순서 편집'에서 편을 위아래로 옮기거나 뺍니다. 키보드로도 똑같이 쓸 수 있고, 빼도 노트는 지워지지 않습니다. 남는 편이 2개보다 적으면 '시리즈 풀기'로 풉니다. 편집하는 사이 다른 곳에서 순서가 바뀌었으면 저장하지 않고 알려 줍니다.
- 보관되었거나 찾을 수 없는 편은 목차에 흐리게 남고, 번호와 이전·다음에서는 빠집니다. 표지를 보관하면 시리즈가 풀립니다.
- 노트 목록에서는 표지에 '시리즈 · 3편', 각 편에 '시리즈 이름 · 2편' 라벨이 붙습니다. 시리즈 이름으로 검색하면 그 편들도 나옵니다.
- AI 지침: 쓰기 지침 42의 핵심에 여러 편으로 나눠야 하는 설명은 시리즈로 쓴다는 내용을 넣었고(8,093자), 쓰는 법은 노트 속성 안내(revision 10)에 있습니다. 각 편을 먼저 쓰고 표지는 마지막에 쓰며, 편 제목에 번호를 넣지 않고 본문에 목차나 다음 편 링크를 넣지 않습니다. 이미 있는 노트도 AI에게 부탁하면 시리즈로 묶습니다.
- MCP 서버는 규칙에 어긋난 시리즈를 규칙 이름(`series.shape`, `series.cover`, `series.chapter`, `series.nested`, `series.taken`)과 함께 거절합니다. 노트 만들기와 고치기, 일괄 고치기, 변경 제안에서 모두 검사합니다.
- 데모 프로젝트에 3편짜리 시리즈를 넣었습니다.
- 배포: 마이그레이션은 없습니다. MCP 함수(검사와 지침)와 사이트를 다시 올립니다.

## 0.68.0 — 2026-10-20

AIs can now mark the sentences a reader must not miss: [sentence]{.key} for the answer a section must keep, .support for evidence, .counter for a contrary result or risk, .unverified for an assumption or unrun check. Each has one look (marker, green, double red, wavy amber) and keeps the text colour. The writing guide allows one key and three marks per section, one per paragraph, one sentence each, and the MCP server refuses an AI write that adds marks past that. People mark and clear them in the editor.

- AI가 페이지의 중요한 문장을 네 가지 뜻으로 칠합니다. 핵심은 형광펜과 굵게, 근거는 초록 밑줄, 반대·위험은 빨간 이중 밑줄, 미확인은 주황 물결 밑줄입니다. 글자색은 그대로라 링크(색 글자)나 용어 설명(회색 점선)과 헷갈리지 않고, 마우스를 올리면 이름이 뜹니다.
- 너무 많이 칠하지 않게 한도를 둡니다. `##` 절마다 핵심 1개와 강조 3개, 문단이나 목록 항목마다 1개, 강조 하나에 한 문장까지이고, 제목·캡션·표·인용·콜아웃·코드에는 칠하지 않습니다. 쓰기 지침(revision 41)이 이렇게 안내하고, MCP 서버는 AI의 페이지 쓰기가 한도를 넘으면 규칙 이름(`emphasis.key` 등)과 함께 거절합니다. 사람이 칠해 둔 강조는 그대로 두고, AI의 쓰기가 강조를 늘릴 때만 거절합니다. 사람이 한도보다 많이 칠한 문단도 AI가 고칠 수 있습니다.
- 편집기에서 직접 칠하고 지울 수 있습니다. 도구 막대의 '강조'나 ⌘/Ctrl+Shift+H로 메뉴를 열고 1–4로 칠하고 0으로 지웁니다. 아무것도 고르지 않았으면 커서가 있는 문장을 칠합니다. 사람이 칠하는 강조에는 개수 제한이 없습니다.
- 편집기에서 굵게 쓴 문장의 일부만 강조하거나 링크를 걸고 저장하면 별표(**)가 그대로 보이던 문제를 고쳤습니다.
- 한 줄 미리보기와 슬라이드에는 표시 없이 글만 남습니다. 화면 낭독기는 '반대·위험: …'처럼 이름을 먼저 읽고, 복사한 글에는 이름이 섞이지 않습니다.
- 차트 문법은 쓰기 지침의 핵심에서 evidence 섹션으로 옮겼습니다. 차트를 그릴 때만 필요한 내용이라, 핵심 지침이 8,074자에서 8,050자로 줄었습니다.
- 배포: 마이그레이션은 없습니다. MCP 함수(검사, 지침, 패널), 사이트, 플러그인을 다시 올립니다.

## 0.67.1 — 2026-10-18

AIs now have one rule set for explaining a visual: say how to read it, what changes, what it means for the research and what is not verified, beside the visual and again in the final reply; keep interactions computed from one state and toy examples labelled. MCP clients read it as get_guide(topic:writing, section:visuals) and the plugin bundles it as a reference. Writers of numbers without a figure are not sent to it.

- AI가 그림이나 인터랙티브 설명을 만들 때 따를 규칙을 한곳에 모았습니다. 그림이 무엇에 답하는지, 어떻게 읽는지, 무엇이 보이거나 바뀌는지, 방법이나 결정에 무슨 뜻인지, 무엇이 확인되지 않았는지를 그림 옆과 최종 답변에 함께 씁니다. 파일·위젯·링크만으로는 설명이 아닙니다.
- 인터랙션은 관계를 더 잘 보여 줄 때만 쓰고, 계산되는 값은 같은 입력 상태에서 함께 바뀌게, 손으로 그린 단계는 그렇다고 밝히게 했습니다. 개념 예시·실측·실행 안 한 제안을 구분하고, 도식이 효과를 입증하지 않는다는 점(설명 분산 ≠ 과제 성능, FLOPs 감소 ≠ 실측 속도)을 적습니다.
- MCP에서는 `get_guide(topic:writing, section:visuals)`로, 플러그인에서는 `visual-explanations.md` 참조로 같은 원본을 읽습니다. explainer·equation 지침과 시각화 지침이 이곳을 가리키고, 숫자나 표만 쓰는 작업은 그림이 있을 때만 읽습니다.
- Codex가 만든 변경을 검토해 넣었습니다. AI가 읽는 문서에서 관리용 문장을 빼고, 섹션을 3,938자에서 2,254자로 줄였습니다.
- 배포: 마이그레이션은 없습니다. 지침이 바뀌었으니 MCP 함수를 다시 올립니다.

## 0.67.0 — 2026-10-18

A question's page puts the evidence it cites under its answer, counter-evidence first, and folds every round before the last three, saying how many still wait to be read. The briefing lists first the changes to what a checked conclusion or an open question cites, and says which. A judgment a person confirmed leads its page. Requests for AI now say to ask the AI to check its queue, which is what makes it take them. The usage history switch says what it counts. The trial's fidelity checks read what a run wrote, not only its numbers.

- 질문 페이지는 '지금까지의 답' 바로 아래에 '이 질문의 근거'를 둡니다. 질문이 인용한 기록을 모두 반대 근거, 불확실, 지지, 계획 순으로 보여 줘서, 근거가 6개를 넘어도 반대 근거가 지지 근거 뒤로 접히지 않습니다. 회차에도 나오는 결과는 여기서는 답에 대해 무엇을 말하는지로, 회차에서는 예측과 나란히 읽힙니다.
- 회차는 최근 3개만 펼치고 그 앞은 하나로 접어 위에 둡니다. 접힌 묶음에는 해석을 기다리는 결과 수나, 질문이 지금 머문 회차의 상태를 적습니다. 0.66.2는 해석을 기다리는 회차를 모두 펼쳐서, 그런 회차가 많으면 다시 전부 펼쳐졌습니다.
- 브리핑의 '지난 방문 이후'는 확인한 결론이나 열린 질문이 근거로 인용한 기록의 변경을 먼저 보여 주고, 제목 아래에 이유를 적습니다('…'에서 확인한 결론의 근거, 메인 질문의 근거, 질문 '…'의 근거). 인용은 먼저 보이는 이유일 뿐, 결론이나 답이 바뀌었다는 뜻은 아닙니다.
- 사람이 확인한 판단이 있으면 선택 이력이 그 페이지 본문 앞에 옵니다. 판단이 없거나 제안·저장 대기뿐이면 전처럼 끝의 정보 묶음에 있습니다. 쓰던 판단 초안은 다른 사람이 첫 판단을 확인해 자리가 바뀌어도 그대로 따라갑니다.
- AI 요청 문구를 바로잡았습니다. 0.66.2의 '다음 세션에 가져갑니다'는 지킬 수 없는 약속이었습니다. AI는 접속할 때 대기열을 알려 받지만 처리까지 정해져 있지는 않아서, 이제 'AI에게 대기열을 확인해 달라고 하면 가져갑니다'라고 씁니다.
- 내 사용 기록 스위치 아래에 무엇을 세는지 한 줄을 둡니다. 화면과 작업 종류별 횟수만 세고, 연구 내용은 남기지 않으며, 로그아웃하면 지워집니다.
- 시험(trial)의 충실 판정이 숫자만이 아니라 쓴 내용을 봅니다. ml-notebook-en은 LongBench의 3.1점 감소를 그 변화에 이어 적었는지, 반대 주장이 섞이지 않았는지 보고, med-literature-ko는 재입원율이 센서군 18.4%, 일반 진료군 27.1%에 바르게 붙었는지 봅니다. 0.67.0 전 기준선과는 충실률을 그대로 비교하지 않습니다.
- 배포: 마이그레이션은 없습니다. 이번 버전 번호를 알리도록 MCP 함수를 다시 올립니다.

## 0.66.2 — 2026-10-18

The privacy policy taking effect on October 25 states the basis for each kind of information, how it is destroyed, and each overseas recipient's contact and legal basis, and corrects three facts: Resend sends sign-up and password emails, the data is stored in Seoul, and Supabase contracts through Supabase Pte. Ltd. The previous policy stays readable. Invitations forget the invited address once used. Wording that lost a condition in 0.66.0 states it again, earlier rounds fold past a waiting one, equation checks must try each variable off 0 and ±1, and the briefing counts the reader's days.

- 개인정보 처리방침(10월 25일 시행)에 법이 공개를 요구하는 항목을 채웠습니다. 정보마다 처리 근거(계약 이행 또는 정당한 이익)를 적었고, 파기 방법과 국외 이전받는 회사의 연락처, 이전 시기와 방법, 근거를 넣었습니다. 실제와 달랐던 세 가지도 바로잡았습니다. 가입·비밀번호 메일도 Resend로 나가고, 데이터베이스는 서울에 저장되며, Supabase의 계약 회사는 Supabase Pte. Ltd.(싱가포르)입니다. 탈퇴 뒤 공동 기록에 남는 계정 번호와 되돌릴 수 없게 바꾼 이메일 값도 사실대로 적었습니다. 이름은 법에 맞춰 '개인정보 처리방침'이 되었고, 첫 화면의 링크는 다른 안내보다 굵게 보입니다.
- 이전 방침(10월 15일~24일)은 `/privacy/ko/2026-10-15`, `/privacy/2026-10-15`에서 그대로 읽을 수 있고, 새 방침의 변경 이력이 그곳을 가리킵니다.
- 가입 문구는 "이용약관에 동의하게 됩니다"까지입니다. 개인정보 처리방침은 동의를 받는 문서가 아니라 공개하는 문서이고, 서비스는 동의가 아니라 계약 이행을 근거로 처리하므로 링크로 보여주기만 합니다.
- 초대는 수락되거나 취소되면 초대받은 이메일 주소와 메시지를 바로 지우고, 30일 뒤에는 기록째 지웁니다. 수락되지 않은 채 기한이 지난 초대는 소유자의 멤버 목록에 30일 동안 남았다가 지워집니다. 매일 새벽에 도는 정리 작업이 맡습니다.
- 0.66.0에서 문구를 줄이다 빠진 조건을 되살렸습니다. AI 요청은 "AI를 연결하면 가져갑니다"가 아니라 "다음 세션에 가져갑니다"이고, 선택 이력의 검토는 승인되어도 Owner나 Semi-Owner가 그 화면에서 확인해야 현재 판단이 됩니다. 예측이 없는 회차는 "예측 없이 실행했습니다"가 아니라 "실행 전 예측 기록 없음"이라고 씁니다. 앱이 아는 것은 기록이 없다는 데까지이기 때문입니다. 디자인 원칙에 이런 조건은 줄여도 남긴다는 줄을 더했습니다.
- 질문 페이지는 오래된 회차 하나가 해석을 기다려도 나머지 정리된 회차를 접습니다. 지금까지는 맨 앞 회차 하나가 기다리면 나머지도 모두 펼쳐졌습니다. 기다리는 회차는 접힌 묶음 밖에 제 번호로 남습니다.
- 수식의 점검값은 다른 값을 가질 수 있는 변수마다 한 번은 0과 ±1이 아닌 값을 써야 합니다. 여러 식이 거기서 같은 값을 내서(x²와 x³은 0과 1에서 같습니다) 그런 점만으로는 확인되는 것이 없었습니다. 지침은 revision 39입니다.
- 브리핑의 '지난 14일 작업 423건'은 기록과 날짜의 짝을 센 값이라 작업 개수로 읽혔습니다. 이제 비율만 보여주고, 날짜도 UTC가 아니라 읽는 사람의 날짜로 셉니다.
- 배포: 마이그레이션 `20261018120000_forget_used_invitations.sql`을 먼저 적용합니다(`npm run -s migration:sql -- 20261018120000`). 수식 점검과 패널이 바뀌어 MCP 함수도 다시 올립니다.

## 0.66.1 — 2026-10-18

The AI connection page now scrolls, so a long list of AIs no longer hides the Allow button, and when the browser stays on the page after you allow or decline, the page says so within three seconds instead of showing the hand-off forever. AIs with the same name are told apart by when they were last used. Rows of the research tree beside many live branches shorten their tags instead of losing the title or running past the card.

- 승인 화면이 스크롤됩니다. 이 앱은 문서 전체가 아니라 화면마다 스크롤하는데, 승인 화면은 높이의 하한만 있어 스스로 스크롤하지 못했습니다. 그래서 AI 목록이 길면 권한과 허용 버튼이 창 아래로 잘렸습니다. 이제 창보다 긴 승인 화면은 위에서부터 시작하고 화면 자체가 스크롤됩니다.
- 허용하거나 거절한 뒤 3초 안에 AI 쪽 페이지로 넘어가지 않으면, 'AI로 돌아가는 중' 대신 '연결을 허용했습니다'와 다음 할 일을 보여줍니다: AI에서 연결됐는지 확인하고 창을 닫고, 안 됐으면 AI에서 다시 로그인. AI의 주소가 늦게 답하거나 답하지 않으면 브라우저가 이 페이지에 남는데, 지금까지는 로딩만 보여서 연결이 끝났는지 알 수 없었습니다. '승인 후 돌아갈 곳'은 버튼 이름에 맞춰 '허용하면 돌아갈 곳'이 되었습니다.
- 연결할 AI 목록이 마지막으로 쓴 시각까지 보여줍니다. 같은 날 다시 로그인해 생긴 같은 이름의 AI를 구별할 수 있습니다. 이름이 앱 이름과 같으면 앱 이름을 한 번만 씁니다.
- 연구 트리에서 살아 있는 가지가 많으면 선이 폭을 많이 차지해 줄의 글자가 쓸 자리가 좁아집니다. 지금까지는 태그와 관련 기록이 줄어들지 않아 제목이 사라지고, '지금' 표시와 관련 기록이 카드 끝에서 잘렸습니다. 이제 줄마다 남은 폭에 맞춰 덜 중요한 것부터 줄입니다: 갈래 종류는 기호만 남기고, 가지 이름은 줄였다가 숨기고, '중요'와 '지금'은 기호만 남기고, 관련 기록은 줄였다가 수를 줄입니다. 제목은 말줄임표로 끝날 뿐 사라지지 않습니다. 소개 페이지의 예시 트리도 휴대폰 폭에서 제목이 보입니다.
- 원격 서버에서 로그인이 `Address in use (os error 98)`로 끝나면 설정에 고정한 콜백 포트를 다른 프로그램이 쓰는 것입니다. 연결 안내의 문제 해결 표에 확인 방법과 다른 포트로 로그인하는 명령을 적었습니다.
- 배포: 웹사이트만 바뀝니다. 마이그레이션과 MCP 함수는 그대로입니다.

## 0.66.0 — 2026-10-18

When an AI tool signs in again, the approval screen now asks which AI it is: a new one, or one of yours, which keeps its name, permissions and project approvals while the connection it used before stops working. Until now each sign-in that registered a new client added another AI without project approvals. The interface's own words were rewritten to read as a person writes them: no sentences glued to labels, no arrows on links, short statuses.

- AI가 다시 로그인하면 승인 화면이 **연결할 AI**를 묻습니다. **새 AI**로 추가하거나 내 OAuth AI 중 하나를 고릅니다. 고른 AI는 같은 AI 그대로라 이름, 권한, 프로젝트 승인, 기록이 이어지고, 그 AI를 쓰던 이전 연결은 끊깁니다. 지금까지는 Codex처럼 로그인할 때마다 OAuth client를 새로 등록하는 도구가 다시 로그인하면 '내 AI'에 프로젝트 승인 없는 AI가 하나씩 늘었습니다.
- 목록에는 같은 앱의 AI가 먼저, 최근에 쓴 순서로 나옵니다. 기본은 새 AI이고, 기존 AI를 고르면 그 AI의 권한이 아래 권한 칸에 채워지며 무엇이 이어지고 무엇이 끊기는지 한 줄로 보입니다. 승인하는 연결이 이미 내 AI 중 하나라면 묻지 않습니다.
- '내 AI'에 같은 AI가 여러 개 있다면 다시 로그인할 때 생긴 것입니다. 쓰지 않는 것은 '내 AI'에서 지우고, 다음 로그인부터 쓰던 AI를 고르세요. 연결 안내의 문제 해결 표에도 적었습니다.
- 화면의 말을 사람이 쓰듯 고쳤습니다. 라벨 뒤에 가운뎃점으로 문장을 잇지 않고, '이름 — 설명'과 링크 끝의 화살표를 없앴습니다. 상태 메시지는 무엇이 일어났고 무엇을 하면 되는지만 씁니다("전달 결과 미확인 · 자동 재요청하지 않습니다…" 대신 "요청이 전달됐는지 확인하지 못했습니다. 다시 보내기 전에 AI 협업의 대기열을 확인하세요."). 제목 아래 설명 문장은 빼고, 주의할 점은 누를 때 보입니다. 영어, 일본어, 프랑스어도 함께 고쳤습니다.
- 소개 페이지의 문구를 새로 썼고("AI와 함께 쓰는 연구 노트"), 예시 창의 설명은 창 아래에 둡니다. 발표 화면에서 메모나 원문 창을 열 때 뒤를 흐리게 하던 효과는 어둡게만 가립니다.
- 이 규칙은 `docs/design-principles.md`의 '화면의 말'에 있고, `src/ui/copyStyle.test.ts`가 모든 화면 문구를 검사합니다.
- 배포: 새 마이그레이션 `20261018100000_continue_oauth_agent.sql`을 먼저 적용합니다(`npm run -s migration:sql -- 20261018100000`). 패널 문구가 바뀌어 MCP 함수도 다시 올립니다.

## 0.65.3 — 2026-10-18

Signing out of the website no longer signs out the AIs connected to your account: it ends that browser's session only, so Codex and Claude Code on other computers stay connected. The plugin no longer needs updating by hand: Codex picks up a new version when it starts, and Claude Code does once auto-update is on for this marketplace. On a remote server, `codex mcp login --no-browser` signs in without port forwarding. You can delete your account yourself from personal settings.

- 웹사이트에서 로그아웃하면 그 브라우저의 세션만 끝납니다. 지금까지는 Supabase의 기본값대로 계정의 모든 세션을 지워서, 다른 컴퓨터의 Codex·Claude Code 연결까지 끊겼고 다음 토큰 갱신에서 다시 로그인해야 했습니다. 비밀번호를 바꾸면 다른 세션이 모두 끝나는 것은 Supabase 서버의 동작이라 그대로입니다.
- 플러그인은 손으로 업데이트하지 않습니다. Codex는 시작할 때 Git 마켓플레이스를 확인해 새 버전을 받고, Claude Code는 이 마켓플레이스의 자동 업데이트를 켜 두면 받습니다. 연결 안내와 플러그인 README가 그렇게 말하고, 다시 설치하라는 안내는 뺐습니다. VS Code나 앱에서 다시 설치하면 Codex가 로그인을 새로 시작하고 '내 AI'에 연결이 하나 더 생깁니다.
- 원격 서버에서는 `codex mcp login research-loop-plugin --no-browser`로 로그인합니다. 나온 주소를 내 컴퓨터 브라우저에서 열어 승인하고, 열리지 않는 `127.0.0.1` 주소를 서버의 터미널에 붙여 넣으면 끝납니다. '내 AI'의 원격 서버 안내도 같은 방식입니다.
- 개인 설정에서 계정을 바로 삭제합니다. 운영자에게 메일을 보내던 절차 대신, 삭제 버튼이 이 계정이 정할 것을 묻고 창을 엽니다: 한 문장, 떠나는 공유 프로젝트, 내가 소유한 공유 프로젝트를 보관할지 지울지, 내보내기 링크, 비밀번호. 비밀번호는 세션을 남기지 않는 클라이언트로 다시 로그인해 확인하고, 서버는 5분 안에 비밀번호로 로그인한 토큰일 때만 지웁니다. 개인정보처리방침의 삭제 항목과 시행일(2026-10-25)을 고쳤습니다.
- 설정 화면들의 제목 아래 설명 문장을 뺐습니다. 버튼이 하는 일은 라벨에, 되돌리기 어려운 일의 결과는 누를 때 여는 확인 창에 있습니다. Google Calendar의 상태는 단어로, 알림은 문장으로 바뀌었고, 빈 목록은 '아직 없음'이라고 씁니다.
- 배포: 새 Edge Function `delete-account`를 올립니다(`npx supabase functions deploy delete-account`, `supabase/config.toml`의 `verify_jwt = true`를 따름). 새 마이그레이션은 없습니다.

## 0.65.2 — 2026-10-17

A release tag now deploys the website and publishes the plugin only after every CI check passes on the tagged commit. Under an equation's result, readers see the exact expression its sliders compute, and an AI that writes one gives two or three values worked out from the TeX: a save computes the expression there and refuses a disagreement. The guidance trial now grades whether a run wrote the request's facts, such as a result's direction and numbers, apart from whether it finished.

- 릴리스 태그를 올리면 그 커밋에서 CI 네 가지(웹, Deno, SQL, e2e)가 모두 통과한 뒤에만 웹사이트를 배포하고 플러그인을 냅니다. 지금까지는 태그와 함께 배포 워크플로가 따로 돌아서, 0.65.1은 SQL 테스트와 e2e 대부분이 그 커밋에서 돌지 않은 채 나갔습니다. Cloudflare의 Workers Builds가 켜져 있으면 이 순서를 건너뛰고 바로 배포하므로 꺼 둡니다(Workers → 설정 → Builds → 연결 끊기). `npm run check:site -- --wait 2400`이 CI와 배포를 기다렸다가 확인합니다.
- 수식의 결과 아래에 실제로 계산하는 식이 그대로 나옵니다(`계산식 B × 3 × s / (2 + s)`). 위의 식이 일반 규칙이고 슬라이더는 그 한 경우를 계산할 때(레이어 셋, 바깥 둘의 민감도 1) 무엇을 계산하는지 읽는 사람이 바로 봅니다.
- AI가 계산식을 쓰면 TeX로 손수 계산한 점검값 두세 개(`evaluate.checks`)를 함께 보내야 합니다. 서버는 그 점에서 계산식을 계산해 1% 넘게 어긋나면 두 값을 밝혀 저장을 거절합니다("B=0.6, s=6에서 계산식은 1인데 점검값은 1.35"). 점검값은 블록에 남아, 페이지를 통째로 다시 쓸 때도 다시 계산하지 않고 대조됩니다. 앱에서 사람이 수식을 고칠 때는 점검값을 요구하지 않고, 남아 있는 점검값만 계산식과 맞는지 봅니다.
- 데모의 예산 식과 가이드 예시가 보여 주는 식 그대로 계산합니다. 예산 슬라이더는 0.4까지이고, 식에 없던 상한(1)을 뺐습니다. 가이드(개정 38)는 계산식의 모든 부분이 TeX에 있거나 라벨·캡션이 말해야 한다고 적고, 소개 페이지의 식은 `196 * …` 대신 `1.96 * … * 100`으로 씁니다.
- 지침 시험에 '충실' 판정이 생겼습니다. 결과의 방향, 핵심 수치, 날짜, 프로젝트 규칙처럼 요청과 기록의 사실을 그대로 옮겼는지를 과제마다 기계적으로 봅니다. 결과를 거꾸로 적고도 완료로 세던 실행은 이제 완료이되 충실하지 않은 실행으로 나옵니다. `summary.md`의 모델별 표에 충실 열이 있고, 완료의 정의는 그대로라 이전 기준선과 비교됩니다.
- 배포: 새 마이그레이션 `20261017100000_equation_checks.sql`을 MCP 함수보다 먼저 적용합니다(`npm run -s migration:sql -- 20261017100000`).

## 0.65.1 — 2026-10-17

Code excerpts for implementation reports no longer read through a symbolic link, so a report cannot carry a file from outside the repository, and a new file nobody asked for (a checkpoint link, a large result file, a nested repository, a Korean file name) no longer stops the excerpt. The ChatGPT request dialog opens on a blank, focused request: suggestions only fill it, and the send button or Cmd/Ctrl+Enter sends. Account and task-assignment emails are in English, in one layout.

- 구현 보고에 코드를 옮겨 오는 도우미(`scripts/code-excerpt.mjs`)가 작업 트리의 심볼릭 링크를 따라가지 않습니다. 저장소 밖 파일(예: `~/.ssh` 아래)이 링크를 타고 보고에 실려 팀 프로젝트에 저장되던 길을 막았습니다. 발췌할 파일은 저장소 안의 5 MB 이하 일반 파일이어야 합니다.
- 발췌를 요청하지 않은 새 파일은 git처럼 세기만 합니다. 체크포인트·데이터 링크(링크는 git이 저장하는 대로 1줄), 큰 결과 파일, 저장소 안의 다른 저장소(0줄), 바이너리 파일(0줄)이 있어도 발췌가 멈추지 않습니다. 한글 이름 파일이 있으면 발췌가 멈추고 바뀐 한글 파일이 따옴표 붙은 이름으로 적히던 문제도 고쳤습니다.
- ChatGPT 요청 창이 빈 입력칸에 커서를 둔 채 열리고, 같은 대상을 다시 열면 쓰던 요청이 남아 있습니다. 쉽게 설명·근거 확인·개선안은 칸을 채우기만 하고, 보내기는 버튼이나 ⌘/Ctrl+Enter로만 합니다. Enter는 줄바꿈이고 한글을 조합하는 중에는 보내지 않으며, 저장하지 않은 편집이 있거나 전달 중일 때는 단축키도 동작하지 않습니다. 선택한 글의 인용은 글을 골랐을 때만 '인용 범위'에 나옵니다.
- 계정 메일(가입 확인, 초대, 로그인 링크, 이메일 변경, 비밀번호 재설정, 재인증 코드, 보안 알림 일곱 가지)과 작업 배정 메일이 같은 영어 양식을 씁니다. 작업 메일은 배정한 사람과 할 일 제목을 이스케이프하고 https 링크만 넣으며, 텍스트 본문도 함께 보냅니다.
- 배포: 작업 메일은 `task-email-worker` 함수를 배포해야 바뀝니다. 계정 메일 템플릿은 지금 값을 백업한 뒤 Supabase의 Email Templates 화면이나 Management API로 직접 넣고(`supabase/templates/README.md`), 보안 알림은 알림마다 켜야 나갑니다. 새 마이그레이션은 없습니다.

## 0.65.0 — 2026-10-17

A model now carries 18 tools on every turn instead of 75: the core tools and three meta tools. The other tools sit in eight groups; describe_tools gives their arguments, and call_tool_read or call_tool_write calls them through the same handler, checks and permissions. One get_guide replaces eleven guide tools. A first sentence that overviews show must fit 180 columns and a new title 120, and writes return what overviews will show, with advice on a missing bottom line, a title in codes or run ids up front.

- 모델이 매 차례 받는 도구 목록이 75개, 약 74,000자에서 18개, 약 24,000자로 줄었습니다. 핵심 도구 15개와 메타 도구 3개(`describe_tools`, `call_tool_read`, `call_tool_write`)만 목록에 두고, 나머지 49개는 records·questions·tree·planning·ai_tasks·reviews·discussions·projects 여덟 그룹에 있습니다. `describe_tools(group)`이 인자를 알려 주고, `call_tool_read`·`call_tool_write`는 직접 부를 때와 같은 처리기·입력 검사·권한으로 부릅니다. 어느 도구든 이름으로 부르면 지금처럼 동작하고, 패널이 부르는 도구는 그대로 목록에 있습니다.
- 가이드 도구 열한 개가 `get_guide({topic, section?, type?})` 하나가 됐습니다. 주제는 writing, record, question, tree, meeting, task_analysis, literature, visualization, workflow, manual이고 예전 도구와 같은 내용을 돌려줍니다. 예전 이름도 계속 동작합니다.
- 개요가 보여 주는 첫 문장은 쓰는 자리에서 지킵니다. 질문의 답, 결과의 뜻, 예측의 첫 문장은 180칸, AI가 새로 짓거나 바꾸는 제목은 120칸 안이어야 하고, 넘으면 규칙(`lead.*`, `title.width`)과 잰 폭·한계를 붙여 거절합니다. 저장된 글을 그대로 다시 보내면 통과하고, 패널에서 사람이 고친 제목은 저장 한도만 봅니다.
- 쓰기가 개요에 어떻게 보일지 돌려줍니다. 연구 기록을 쓰는 도구는 결과에 `readBack`(개요에 나갈 글)과 `advice`(핵심 결론이 없음, 코드뿐인 제목, 맨 앞의 실행 ID·경로)를 싣습니다. 조언은 쓰기를 막지 않고, 지침 계수기가 `advised`로 셉니다.
- 접속 지침이 목록에 없는 도구를 부르는 법과 쓰기 전에 읽을 `get_guide` 주제를 알려 줍니다(2,139자에서 2,125자로). 도구 설명·가이드·오류와 앱의 AI 요청 문구(네 언어)도 `get_guide`를 가리킵니다.
- 지침 시험은 `call_tool_*` 호출을 그것이 닿은 도구로 채점하고, 쓰기가 받은 조언 가운데 마지막 상태에서 고친 몫을 모델별로 보여 줍니다. 기준선(v0.64.3)과 같은 날 `npm run guide:eval -- --hosts claude,codex`로 비교합니다.
- 새 마이그레이션은 없습니다. MCP 함수만 배포합니다.

## 0.64.3 — 2026-10-17

Some Claude Code versions end a run that met the plan's usage limit with the limit message as an ordinary answer. The cross-model trial now reads such a message, given before any tool call, as the limit: the run is set aside and Claude Code's remaining runs are skipped, instead of each counting as the model failing its task. The guidance is unchanged.

- 사용 한도를 보통 답처럼 내놓는 Claude Code도 한도로 봅니다. 일부 버전은 한도에 닿은 실행을 오류가 아니라 답("You've hit your limit …")으로 끝내는데, 지금까지는 그 실행과 뒤의 실행이 모두 모델이 과제를 못 한 것으로 셈됐습니다. 도구를 하나도 부르기 전의 한도 문구는 이제 CLI의 한도로 보고, 그 실행은 수치에서 빼고 남은 실행은 건너뜁니다.
- 실제 Claude Code에 시험 도구를 하나 부르는 각본 응답을 이 기계 안에서 돌려, 권한 설정 아래에서 도구 호출이 통하고, 시험 서버가 그 호출을 기록하고, 토큰이 실행 전체로 합산되는 것을 확인했습니다.
- 지침 시험의 기준선은 이 버전으로 잽니다(`git checkout v0.64.3`).

## 0.64.2 — 2026-10-17

The cross-model trial now runs through Claude Code and Codex logged in with your own subscription: npm run guide:eval -- --hosts claude,codex. No API key is used or billed. Each task runs once in an empty folder, with the trial server as the CLI's only MCP server and the CLI's own tools, instruction files and memory off. A login that bills per token is refused before the first run, and a usage limit stops that CLI's remaining runs. The guidance itself is unchanged.

- 교차 모델 시험이 구독으로 돕니다. `npm run guide:eval -- --hosts claude,codex`가 과제마다 Claude Code(`claude -p`)와 Codex(`codex exec`)를 한 번씩 띄웁니다. API 키도 토큰 과금도 없고, 각 CLI에 로그인된 구독의 사용량만 씁니다. 모델은 `--hosts claude:opus,codex:<모델>`처럼 고릅니다.
- 과금될 일은 미리 막습니다. CLI는 키 환경 변수를 지운 채 실행되고, 시작 전에 로그인을 확인해 API 키나 클라우드 공급자 로그인이면 그 CLI를 돌리지 않습니다. CLI가 사용량 한도를 알리면 그 CLI의 남은 실행은 건너뜁니다.
- 실행마다 격리합니다. 저장소 밖의 빈 폴더에서 CLI를 띄우고, 시험용 MCP 서버 하나만 연결하며, CLI 자체 도구(셸·파일·웹)와 CLAUDE.md·메모리·사용자 설정은 끕니다. Codex는 `~/.codex/AGENTS.md`를 끄는 설정이 없어 그 파일이 있으면 돌리지 않습니다. 실제 두 CLI가 보내려던 요청을 이 기계 안에서 받아 확인했습니다.
- 모델 탓이 아닌 멈춤은 수치에서 뺍니다. 사용 한도, CLI가 더한 도구, 한 실행에 시험 서버가 둘 뜬 경우(Codex의 하위 에이전트)는 `멈춘 실행`에 이유와 함께 적고 모델별 수치에는 넣지 않습니다.
- 지침은 바꾸지 않았습니다. 도구 목록과 접속 지침은 0.64.1과 바이트 단위로 같습니다. 0.65.0의 지침 개편은 이 시험으로 기준선을 잰 뒤 같은 날 같은 방법으로 비교합니다.

## 0.64.1 — 2026-10-17

The cross-model trial now meets production's rules where a model can trip on them: a key reused for a different write is refused, and a week plan makes an earlier planning token stale. A provider request that never answers ends the run as an error after ten minutes instead of hanging the trial, and Claude requests cache the tool list and instructions, so later turns cost less. Token counts are unchanged.

- 시험용 프로젝트가 운영과 같은 곳에서 거절합니다. 같은 키를 다른 쓰기에 다시 쓰면 운영처럼 `invalid_request`로 거절되고(지금까지는 앞의 영수증을 돌려줘 성공처럼 보였습니다), 구현 보고의 요청 키는 그 보고의 것입니다.
- 일정 맥락이 운영과 같은 모양입니다. 끝난 일은 빠지고, 맡은 사람이 없으면 `unassigned`, 캘린더는 `disabled`, 그리고 주간 예산이 들어가 주간 계획을 세운 뒤에는 그 전에 읽은 계획 토큰이 운영처럼 낡은 것이 됩니다.
- 공급자가 10분 동안 답하지 않는 요청은 네트워크 실패로 보고 다시 보낸 뒤, 끝내 답이 없으면 그 실행만 오류로 남깁니다. 지금까지는 시험 전체가 멈춰 있을 수 있었습니다.
- Claude 요청은 도구 목록과 접속 지침을 프롬프트 캐시에 올립니다. 실행의 두 번째 차례부터 이 부분은 캐시 요금으로 읽히고, 세는 토큰 수는 그대로입니다.

## 0.64.0 — 2026-10-17

Measurement before the guidance changes. A field refused for its width now names the rule, and the MCP server counts each tool call's outcome per day by AI client, tool and rule, keeping nothing an AI wrote and no project or person. npm run guide:eval runs ten tasks in Korean and English against Claude, GPT and Gemini models through the real MCP handlers over an in-memory project, and grades what each one saved. The guidance itself is unchanged.

- 거절이 규칙을 밝힙니다. AI가 쓴 짧은 칸이 너비를 넘어 거절되면 오류에 `writing.answer`, `writing.prediction`처럼 어떤 규칙인지가 붙습니다. 메시지 문장은 그대로입니다.
- 지침 계수기. MCP 서버가 답한 도구 호출마다 결과 하나를 셉니다. 성공, 규칙별 거절(규칙이 없으면 `code:<오류 코드>`, 인자가 도구의 형식에 맞지 않으면 `schema`)이고, 하루에 AI 종류·도구·결과·규칙마다 한 줄입니다. 응답을 보낸 뒤에 기록하므로 기록이 실패해도 도구 결과는 그대로입니다. AI가 쓴 글, 인자, 프로젝트, 사람, 키는 남기지 않습니다. 주간 조회 SQL은 `docs/MCP.md`에 있습니다. 마이그레이션 `20261016140000_mcp_guidance_counts.sql`이 필요합니다.
- 교차 모델 시험. `npm run guide:eval`이 과제 열 개(한국어 다섯, 영어 다섯, 생물·사회과학·시스템·기계학습·화학·물리·의학·소프트웨어·일정)를 모델마다 돌립니다. 모델은 실제 MCP 처리기에 연결된 메모리 속 시험 프로젝트에서 도구를 부르고, 무엇이 저장됐는지를 기계적으로 채점합니다. 과제마다 완벽한 답안의 호출이 있어, 테스트가 열 과제 모두 실제 처리기로 끝까지 해낼 수 있음을 확인합니다.
- 비용을 먼저 봅니다. 모델마다 짧은 확인 요청을 먼저 보내 키나 모델 이름이 틀리면 그 모델만 건너뜁니다. 누적 토큰이 `--budget-tokens`에 닿으면 남은 실행은 돌리지 않고, `--dry-run`은 키 없이 과제와 모델마다 도구 목록의 크기와 토큰 하한을 보여 줍니다. 키는 결과 파일과 로그에 남지 않습니다.
- 지침은 바꾸지 않았습니다. 접속 지침과 도구 목록은 0.63.0과 바이트 단위로 같습니다. 지침을 고치는 일은 이 시험으로 기준선을 잰 뒤 0.65.0에서 합니다.

## 0.63.0 — 2026-10-16

Short fields now say one thing. Overviews show the first sentence of an answer, an open question, a prediction or a result, and the whole text stays on its page; a long prediction folds to what it expects, a to-do's completion criterion to two lines. Rows state facts instead of instructions, and sentences that repeated a label are gone. AIs are held to the same: an answer, a finding or a prediction written now must fit a width counted in columns (a Korean character takes two), and the error says what to cut; stored text passes unchanged.

- 브리핑, 연구 흐름, 위쪽의 큰 방향 막대, 회차 요약, 다음 할 일이 지금까지의 답·남은 의문·예측·결과를 첫 문장으로 보여 줍니다. 연구 흐름에서 지금 다루는 질문의 답만 두 문장입니다. 온전한 글은 질문과 기록의 페이지에 그대로 있습니다.
- 실험 페이지의 예측과 판단 기준이 길면 무엇을 예상하는지 한 문장과 '전체 보기'로 보입니다. 할 일 목록의 완료 기준은 두 줄까지 보이고, 가리키거나 고치면 다 열립니다. 두 줄 아래로 세 번째 줄 윗부분이 비치던 문제도 고쳤습니다.
- 접힌 글의 미리보기가 문장이 끝나는 자리에서 끝나고, '전체 보기'가 마지막 낱말 뒤에 붙습니다. 지금까지는 긴 미리보기 옆으로 밀려 '전체 보 / 기'처럼 세로로 끊겼습니다.
- 다음 할 일의 아래 줄이 방법 대신 사실을 말합니다. '밀린 일 2개 정리'에는 어떤 일인지, 오래 실행 중인 실험에는 '12일째 실행 중', 근거가 없는 주장에는 '연결된 근거 없음'이 붙습니다. 팀원의 AI가 물은 질문은 누가 물었는지만 적습니다.
- 반복되던 안내 문장을 뺐습니다. '큰 할 일 추가'와 '하위 할 일 추가' 옆의 설명, 연구 흐름의 빈 단계 문장(이제 '아직 없음'), 브리핑과 연구 흐름의 회차에 붙던 예측 안내와 '예측 없이 실행했습니다'입니다. 예측을 왜 미리 적는지는 질문 페이지가 계속 말합니다.
- 기록 페이지 위의 연구 트리 줄이 가지 이름과 '지금'만 보여 줍니다. 앞 걸음은 새 가지·수정·다시 실험처럼 보통의 다음 걸음이 아닐 때만 적고, 트리에 없는 기록에는 '트리에 놓기'만 있습니다.
- AI가 지금 쓰는 짧은 칸에 길이 한도가 생겼습니다. 지금까지의 답, 결과가 질문에 말해 주는 것, 질문의 배경은 240칸, 남은 의문은 160칸, 예측과 판단 기준은 300칸, 할 일의 완료 기준은 200칸입니다. 한글은 두 칸, 영문은 한 칸으로 세서 언어마다 거의 같은 폭입니다. 넘으면 저장하지 않고 몇 칸인지와 나머지를 어디로 옮길지 알려 줍니다. 이미 저장된 글은 그대로 다시 보내면 통과하므로, 예전에 쓴 노트와 할 일도 고치지 않고 이어서 쓸 수 있습니다.
- AI 지침에 '짧은 칸은 한 가지 생각, 주장 먼저'를 넣고, 완료 기준을 '끝나면 무엇이 남는가' 한 문장으로 쓰게 바꿨습니다(쓰기 지침 36판). 범위와 증거가 모자랄 때의 처리는 설명으로 옮깁니다. 접속할 때 보내는 지침과 도구 목록은 정해 둔 크기 안에 있습니다.

## 0.62.0 — 2026-10-16

The landing downloads about 40% fewer bytes. Its text now comes from a handful of font files instead of dozens of slices: the interface's own face holds its Latin, symbols and every Hangul syllable its messages write, and one small serif slice per weight holds the landing's examples. In Korean the page went from 36 font files (760 KB) to 6 (298 KB), in English from 16 (392 KB) to 3 (104 KB). The to-do page lines up every table and group heading on one set of columns where no text runs into the next, and wraps long titles. A pointed-at symbol's ring in an equation is no longer clipped.

- 처음 여는 소개 페이지가 훨씬 가벼워졌습니다. 한국어 페이지가 글꼴 파일 36개(760 KB)를 받던 것을 6개(298 KB)로, 영어 페이지는 16개(392 KB)를 3개(104 KB)로 줄였습니다. 페이지 전체로는 한국어 1.11 MB → 653 KB, 영어 758 KB → 472 KB입니다.
- 화면 글꼴(Pretendard)에서 앱이 실제로 쓰는 글자만 두 파일로 잘라 냈습니다. 하나는 네 언어의 라틴 문자와 기호, 다른 하나는 앱의 모든 한국어 문구에 쓰인 음절과 자주 쓰이는 음절입니다. 그 밖의 한글은 지금처럼 필요할 때 받습니다.
- 소개 페이지의 연구 예시에 쓰인 명조(마루 부리) 글자만 담은 작은 파일을 따로 만들어, 예시 몇 줄 때문에 명조 파일 15개를 받던 일이 없어졌습니다.
- 글꼴에 없던 기호(◎ ⠿ ↶ ↷ ⑂ ✕)를 아이콘으로 바꿨습니다. 연구 트리의 '지금' 표시, 끌어서 옮기는 손잡이, 되돌리기와 다시 하기입니다. 기기마다 다른 글꼴로 그려지거나 쓸데없는 파일을 받는 일이 없습니다.
- 할 일 페이지의 모든 표와 묶음 제목이 같은 열을 씁니다. 담당자, 진행, 근거와 동작 버튼, 삭제가 페이지 위아래로 한 줄에 섭니다. 묶음 제목의 체크와 제목, 담당자, 진행(하위 할 일 몇 개 완료), 버튼도 그 아래 행과 같은 자리에 있습니다. 진행할 것이 하나도 없으면 진행 열은 자리를 차지하지 않습니다.
- 창이 좁아(약 860px 아래) 열이 제목을 누르면 행이 카드로 바뀝니다. 마우스를 쓰는 기기에서는 분석·편집 버튼이 제목 줄에 함께 놓여, 빈 줄이 생기지 않습니다. 제목 아래 줄은 모두 제목 글자가 시작하는 자리에서 시작합니다.
- 할 일 표에서 '묶음 담당'이 옆 칸의 근거 제목 위에 겹쳐 찍히던 문제를 고쳤습니다. 칸마다 내용이 그 칸 안에서 줄을 바꾸고, 긴 이름은 말줄임으로 줄어듭니다. 내 진행 상태도 메뉴 안에서 '결..'처럼 잘리지 않고 글자로 다 보입니다.
- 하위 할 일의 근거 칸에 자기가 속한 묶음(상위 할 일)의 제목이 근거로 뜨던 문제를 고쳤습니다. 묶음과 그 하위 할 일은 서로의 근거로 세지 않습니다.
- 하위 할 일의 '묶음 담당'은 그 묶음에 담당자가 있을 때만 보입니다.
- 긴 할 일 제목이 잘리지 않고 줄을 바꿔 다 보입니다. Enter는 지금처럼 저장하고, 제목에 줄바꿈이 들어오면 띄어쓰기로 바뀝니다.
- 수식에서 기호를 가리킬 때 그리는 테두리가 줄 맨 앞에서 잘리거나 옆의 = 기호에 닿던 문제를 고쳤습니다.
- 연구 흐름으로 가는 탭 이름을 '흐름'에서 사이드바·페이지 제목과 같은 '연구 흐름'으로 맞췄습니다.
- 긴 페이지 끝의 보이지 않는 안내 문구가 페이지를 늘려, 화면 뒤쪽이 스크롤되던 문제를 고쳤습니다.

## 0.61.0 — 2026-10-16

An implementation report now opens with what it amounts to, in a sentence or two, and a map: the instruction's sentences on the left, the changed code on the right, a line from each sentence to the file that carries it, and the changes nobody asked for standing apart with no line. Pointing at a row lights what it is joined to, and every row opens its item. The list draws each report as its sentences and the changes beyond them. Equations with a term in a bare superscript showed their TeX source; they are typeset again.

- 구현 확인 보고가 네 개의 숫자 칸 대신 두 가지로 시작합니다. 먼저 보고가 무엇을 뜻하는지 한두 문장으로 말하고(지시 몇 문장이 의도대로 됐고 몇 문장이 결정을 기다리는지, 요청 밖 변경 중 몇 곳이 결과나 평가에 닿는지, 보고에 설명이 없는 파일이 있는지), 이어서 지도를 보여 줍니다. 결정을 기다리는 부분에는 형광펜이 칠해집니다.
- 지도는 지시의 문장을 왼쪽에, 바뀐 코드를 오른쪽에 두고 문장마다 그 일을 하는 파일로 선을 잇습니다. 요청 밖 변경은 선 없이 따로 서 있어서, 지시하지 않은 곳에서 무엇이 바뀌었는지가 한눈에 보입니다. AI가 정한 곳의 선은 진하게, 지시와 다르거나 일부만 한 곳은 경고색으로, 의도대로 된 곳은 옅게 그립니다. 문장 끝의 동그라미는 어떻게 확인했는지(테스트 통과, 실행, 코드만 읽음)를 채운 정도로 보여 줍니다.
- 행에 마우스를 올리면 그 문장과 선, 이어진 파일이 밝아지고 나머지는 흐려집니다. 파일에 올리면 그 파일이 맡은 문장이 모두 밝아집니다. 행을 누르면 아래의 그 항목으로 가서 잠깐 표시되고, 의도대로 된 문장은 코드가 펼쳐진 채로 열립니다. 휴대폰에서는 두 열이 위아래로 놓이고 문장마다 파일 이름과 줄이 붙습니다.
- 구현 확인 목록의 각 행이 보고를 작은 칸으로 그립니다. 문장마다 한 칸, 그다음 결과나 평가에 닿는 요청 밖 변경과 설명 없는 파일이 이어지고, 이미 정한 항목은 흐려집니다. 이 그림은 DB 마이그레이션 `20261016120000_implementation_list_items`를 적용한 뒤에 보이고, 그 전에는 지금처럼 숫자로 보입니다.
- 마이그레이션을 SQL Editor에 붙일 SQL을 만들어 주는 `npm run -s migration:sql`이 생겼습니다. 파일 내용을 한 트랜잭션으로 감싸, 앞선 마이그레이션이 기록에 없거나 이미 적용된 경우 아무것도 바꾸지 않고 멈추고, 끝에서 마이그레이션 기록에 스스로를 남깁니다.
- 수식에서 `\sum_{c=1}^d`처럼 중괄호 없이 쓴 위첨자 자리의 기호를 용어로 표시하면, 수식 전체가 그려지지 않고 원문 TeX가 보이던 문제를 고쳤습니다. 다른 이유로 표시가 거부되더라도 표시만 빼고 수식을 그리며, 앱이 넣는 내부 표시는 화면에 나오지 않습니다.

## 0.60.1 — 2026-10-16

Lists read title first. In record, note, discussion and implementation-check lists, a title is set in the serif's SemiBold at 16px, the conclusion or defining line under it at 13px in a lighter ink, and the facts that tell records apart at 12px, so the title no longer reads like one more line. An AI can now give a record only one of its type's statuses: a made-up one such as "reviewed" is refused with the statuses to use, and papers already marked that way show as Reviewed in the reader's language. Returning to a list keeps focus on the row you left.

- 기록 목록에서 제목과 그 아래 설명의 크기가 거의 같아 헷갈리던 문제를 고쳤습니다. 제목은 16px 세리프 굵은 글씨, 그 아래 결론이나 정의 한 줄은 13px 회색, 기록을 구별하는 사실(학회·연도, 카테고리, 질문)은 12px로 한 단계씩 작아집니다. 문헌·질문·방법·데이터셋·실험·분석·논문과 노트 목록이 모두 같습니다.
- 결론이 쓰인 기록은 설명 줄이 검게, 아닌 기록은 회색으로 보이던 것을 같은 색으로 맞췄습니다. 결론에는 지금처럼 뒷받침·반박·확인 중 같은 판정 단어가 붙습니다.
- 토론 목록, 구현 확인 목록, 최근 추가의 기록 제목도 같은 크기와 굵기로 맞췄습니다. 연구 트리, 연구 흐름, 모든 기록의 한 줄 목록은 그대로입니다.
- AI가 기록의 상태를 그 유형에 없는 말로 적지 못합니다. 예를 들어 문헌을 reviewed로 만들려 하면 서버가 planned · active · done 중에서 고르라고 알려 주며 거절합니다. 이미 reviewed로 적힌 문헌은 목록과 페이지에서 '검토됨'으로 보이고, 완료로 바꿀 수 있습니다.
- 구현 확인 보고에서 목록으로 돌아오거나 페이지를 닫을 때, 키보드 초점이 방금 보던 행이 아니라 화면 처음으로 가는 경우가 있던 문제를 고쳤습니다.
- 구현 확인에서 문장을 눌러 할 일 안의 그 자리를 열면 문장에 표시가 되는데, 페이지가 곧바로 다시 그려지며 표시가 사라지는 경우가 있던 문제를 고쳤습니다. 토론에서 인용한 원문을 열 때도 같습니다.

## 0.60.0 — 2026-10-16

When an AI changes code for a to-do or an AI request, it now reports each instruction sentence beside the line of code that carries it and how that was checked, plus what it decided itself, changes nobody asked for and what it could not check. The server checks what it can without trusting the AI. A new Implementation check tab in AI collaboration lets the researcher decide each item beside its code and send the decisions back to the same AI as one request.

- AI 협업에 구현 확인 탭이 생겼습니다. AI가 할 일이나 AI 요청을 하며 코드를 바꾸면, 끝내기 전에 지시의 문장마다 그 일을 하는 코드 줄과 확인 결과를 여기에 보고합니다. 결정할 것이 있는 보고가 위에 오고, 탭에 내 결정을 기다리는 보고의 수가 나옵니다.
- 보고는 지시의 문장을 왼쪽에, 그 문장을 하는 코드를 오른쪽에 둡니다. 그 일을 하는 한 줄에 형광펜이 칠해지고, 바뀐 줄에는 +와 −가 붙습니다. 할 일에 그대로 있는 문장은 연구자의 글씨체로, 대화에서 AI가 옮겨 적은 문장은 'AI가 옮긴 말'로 보입니다.
- 지시와 다르게 했거나 지시에 없던 것을 AI가 정한 곳, 일부만 했거나 빠뜨린 곳, 결과나 평가에 닿는 요청 밖 변경을 하나씩 정합니다. 이대로 두면 두 줄로 접히고, 바꾸게·마저 하게·되돌리게 하면 덧붙일 말을 적을 수 있으며 AI가 든 다른 선택지를 눌러 채울 수 있습니다. 확인 못 한 것은 확인하게 할 수 있습니다.
- 정한 것은 한 번에 보냅니다. 그 일을 한 AI의 작업 대기열에 요청 하나로 들어갑니다. AI가 다시 보고하면 같은 기록의 다음 보고가 되고, 그대로인 항목의 결정은 이어지며 바뀐 항목은 '새로 바뀜'으로 다시 기다립니다. 보낸 요청을 AI가 하지 않고 다시 보고하면 그렇다고 알려 줍니다.
- 서버가 AI를 믿지 않고 직접 확인합니다. 문장이 할 일에 그대로 있는지, 보고가 설명하지 않은 파일이 있는지, 요청 밖에서 테스트·평가 코드를 바꿨는지 봅니다. 요청 밖에서 평가 코드를 바꾸고 알리지 않은 보고는 받지 않습니다.
- 결정은 일을 맡긴 사람과 Owner·Semi-Owner가 합니다. 결정을 기다리는 보고는 알림 하나로 오고, 보고를 열거나 마지막 항목을 정하면 읽음이 됩니다.
- AI용 도구 report_implementation과 get_implementation_report, 쓰기 지침의 구현 절이 생겼습니다. Claude Code·Codex 플러그인에는 git에서 코드 줄을 그대로 옮겨 오는 도우미(scripts/code-excerpt.mjs)가 들어 있습니다.

## 0.53.0 — 2026-10-16

A question's page now reads as the rounds that tested it, in order: prediction, result, meaning and next move, with the step that waits holding what to do. Each prediction shows whether it was written before its result, keeps the sentence a result was read against if it changed afterwards, and is not read as a prediction if first written after. The server no longer lets an AI change a prediction once a result exists. An answered question no longer shows steps it never went through.

- 질문 페이지가 그 질문을 시험한 회차들로 열립니다. 실험 하나가 한 회차이고, 예측 · 결과 · 해석 · 다음이 한 줄씩 순서대로 놓입니다. 한 회차의 다음 수가 다음 회차가 됐으면 두 회차를 가는 선으로 잇습니다. 지난 회차는 접히지만, 아직 기다리는 것이 있는 회차는 접히지 않습니다.
- 회차가 기다리는 칸에 할 일이 있습니다. 아무도 읽지 않은 결과에는 해석 기록, 실행 전인데 예측이 없는 실험에는 예측 적기, 아직 아무 실험도 없는 질문에는 실험 계획하기가 있습니다. 실험 계획하기는 실험을 질문에 이어 만들고, 실행 전에 예측을 함께 적게 합니다.
- 예측 아래에 그 예측이 결과보다 먼저 쓰였는지가 나옵니다. 결과 전에 적었으면 날짜와 함께 '결과 전에 적음', 결과가 나온 뒤 고쳤으면 '결과 뒤 고침'과 함께 결과가 비교된 원래 문장을, 결과 뒤에 처음 적었으면 '결과 뒤 적음'을 보여 주고 그 결과는 예측대로가 아니라 질문에 대한 뒷받침·반대 근거로 읽습니다.
- 결과가 나온 실험의 예측은 AI가 더는 바꿀 수 없습니다. 가설의 예측도 그 가설을 시험한 실험에 결과가 나오면 마찬가지입니다. 서버가 거절하면서, 바뀐 기대는 다음 실험에, 바뀐 가설은 새 가설로 적으라고 알려 줍니다. 사람은 여전히 고칠 수 있고, 고치면 페이지에 결과 뒤 고침으로 남습니다.
- 브리핑과 연구 흐름은 지금 회차를 같은 모양으로 보여 줍니다. 진행률처럼 읽히던 고리는 없앴습니다.
- 결과 해석 창이 짧아졌습니다. 위에 회차가 그대로 있고 판정, 이 결과가 말해 주는 것, 다음 수 순서로 적습니다. 지금까지의 답과 남은 의문은 접혀 있다가 답 정리를 고르면 열립니다.
- 답 정리만 한 질문이 거치지 않은 단계까지 모두 지난 것처럼 보이던 문제를 고쳤습니다. 같은 실험의 나중 결과를 앞 결과의 다음 수로 세던 문제도 고쳤습니다.
- 사이트 검사를 비롯한 스크립트가 macOS에서 심볼릭 링크 경로로 실행되면 아무것도 하지 않고 성공으로 끝나던 문제를 고쳤습니다. 플러그인의 이미지 업로드 도우미도 같습니다.

## 0.52.0 — 2026-10-15

Tables now read as scatter plots and heatmaps as well as line, bar and dot charts: a scatter places each row by a column of numbers, on a log scale when sizes span orders of magnitude, and a heatmap colours every cell on one scale with the best value in bold. Explainers gain four layouts the app places by itself (a map of relations, a tree, a timeline and a cycle), so an AI states structure instead of positions. The visualization guide starts from the reader's question and says first what a page draws without an image.

- 표 그림에 산점도와 히트맵이 생겼습니다. 산점도는 숫자 열 하나를 가로축으로 삼아 행마다 점을 찍고, 모델 크기처럼 자릿수가 다른 값은 로그 눈금으로 읽습니다. 점이 많지 않으면 이름이 점 옆에 붙고, 강조한 점은 강조색 원 위에 놓입니다. 셀의 ±는 가로·세로 오차 막대가 됩니다.
- 히트맵은 표의 모든 칸을 한 색 척도로 칠하고 값을 칸 안에 적습니다. 0을 사이에 둔 변화량은 두 색으로 나뉘고, 좋은 방향을 정하면 가장 좋은 값이 굵게 보입니다. 단위가 다른 열을 섞으면 그리지 않고 이유를 알려 줍니다. 행을 가리키면 그 행의 값이 칸 색과 함께 나오고, 위아래 화살표로도 행을 옮겨 읽습니다.
- 단계별 도해에 모양이 네 가지 더 생겼습니다. 관계도는 연결만 적으면 앱이 왼쪽에서 오른쪽으로 놓고, 계층은 각 부분의 상위만 적으면 되고, 타임라인은 시점을 적은 순서대로, 순환은 2~8개 부분이 고리를 이루며 마지막에서 처음으로 돌아갑니다. AI는 위치 대신 구조만 적고 그림은 앱이 그립니다.
- 계층은 넓은 화면에서 위에서 아래로, 잎이 많으면 왼쪽에서 오른쪽으로, 좁은 화면에서는 들여쓴 목록처럼 그려져 이름이 잘리지 않습니다. 타임라인은 좁으면 위에서 아래로 흐릅니다. 관계도에서 여러 단을 건너는 연결은 다른 부분 위를 지나지 않고 자기 자리로 갑니다.
- 한 단계에서 강조한 부분이 둘 이상이면 그 부분들 사이의 연결만 강조색이 됩니다. 하나만 강조하면 지금처럼 닿는 연결이 함께 강조됩니다.
- SnapKV, StreamingLLM처럼 끊을 수 없는 이름은 상자 여백을 조금 써서 한 줄에 둡니다.
- 시각화 가이드가 독자의 질문에서 시작합니다. "어느 조건이 더 높은가?"에는 막대 표 그림, "어떤 조합이 결과를 가장 바꾸는가?"에는 히트맵, "무엇이 무엇으로 나뉘는가?"에는 계층 도해처럼 페이지에서 바로 그리는 방법을 먼저 알려 주고, 이미지는 논문·발표용이거나 페이지가 그릴 수 없는 그림에만 씁니다. 앱의 시각화 가이드도 유형마다 페이지에서 그리는 방법을 먼저 적습니다.

## 0.51.0 — 2026-10-15

Research Loop now speaks English, Japanese and French as well as Korean. Signed-out pages open in English until a device picks a language; the workspace follows the language saved on your account, so every device agrees, and accounts made before this release stay in Korean until you change it in personal settings. Dates, numbers and durations follow the language, and the ChatGPT and Claude panels speak the language of the app they open in. AIs pay about 28% fewer tokens for the tool list on every turn.

- 한국어, English, 日本語, Français로 쓸 수 있습니다. 개인 설정에서 언어를 고르면 계정에 저장되어 다른 기기에서도 같은 언어로 열립니다. 번역을 다 마친 언어만 목록에 나옵니다.
- 이전부터 쓰던 계정은 지금처럼 한국어로 열립니다. 다른 언어로 쓰려면 개인 설정에서 한 번 바꾸면 됩니다. 새 계정은 가입한 기기에서 고른 언어로, 고른 적이 없으면 브라우저 언어로 시작합니다.
- 로그인 전 화면은 영어로 열리고, 화면의 언어 선택으로 바꿀 수 있습니다. 이 기기에서 고른 언어는 다음에도 그대로입니다.
- 날짜, 숫자, 비율, 예상 시간이 언어에 맞게 표기됩니다. 프랑스어는 "1,5 h", "J-3"처럼, 일본어는 "あと3日"처럼 씁니다.
- 할 일 빠른 추가가 언어마다 날짜 표현을 알아듣습니다. "tomorrow", "明日", "demain", "+3", "来週月曜" 모두 됩니다. 프랑스어처럼 일/월 순서로 쓰는 언어에서는 "12/10"을 10월 12일로 읽습니다.
- Google Calendar에 만드는 캘린더와 마감 일정 이름이 계정 언어를 따릅니다.
- ChatGPT·Claude 안의 Research Loop 패널이 그 앱의 언어로 보입니다. 패널에서 AI에게 보내는 요청 문구도 같은 언어입니다.
- AI 연결 안내에 영어 페이지(/guide/ai)가 생겼고 한국어 안내는 /guide/ai/ko로 옮겼습니다. 내 AI 화면의 안내 링크는 쓰는 언어에 맞는 쪽을 엽니다.
- 최근 추가의 종류 칸이 언어에 맞는 너비가 되어 "Groupe de tâches", "データセット" 같은 이름이 줄바꿈되지 않고, 제목도 날짜 묶음과 상관없이 가지런히 놓입니다.
- AI가 매 턴 다시 읽는 도구 목록이 약 22,600토큰에서 16,200토큰으로 줄었습니다. 형식이 이미 말해 주는 정규식, AI가 읽은 값을 복사만 하는 ID의 패턴, 도구마다 붙던 스키마 버전 줄처럼 모델이 쓰지 않는 정보를 뺐고, 실제 호출은 전과 같은 기준으로 검사합니다. 패널 전용 도구는 설명을 한 줄로 줄였습니다.
- 시각화 기법 안내가 같은 규칙을 두 언어로 반복하지 않아 한 번 읽는 데 드는 토큰이 약 30% 줄었습니다. 쓰기 뒤에 붙는 영향 확인 안내도 짧아졌습니다.

## 0.50.0 — 2026-10-15

AI writes take fewer steps. A write now conflicts only with changes to the record it writes, so teammates' edits elsewhere and an AI's own earlier calls no longer force a reload. A page and its bottom line are saved in one call, and update_research_objects edits up to 20 records at once. Rate-limit and expired-token replies say what to do next. Experiment pages keep run problems apart from findings, literature pages say whether the full text or only the abstract was read, and equation symbols match however their braces are written.

- AI가 기록을 고칠 때 충돌을 그 기록 기준으로 판단합니다. 팀원이 다른 페이지를 고쳤거나 같은 AI가 방금 다른 기록을 고쳤다고 해서 다시 읽고 다시 보낼 필요가 없습니다. 질문 노트, 연구 트리, 할 일처럼 정확한 최신 상태가 필요한 기록은 지금처럼 확인합니다.
- 페이지 본문과 핵심 결론을 한 번에 저장해서, 목록에 보이는 요약이 본문보다 오래될 일이 없습니다.
- AI가 여러 기록을 한 번에(최대 20개) 고치고, 실패한 항목만 다시 보낼 수 있습니다. 영향 확인도 작업이 끝난 뒤 한 번만 합니다.
- 요청이 너무 많을 때는 몇 초 기다리면 되는지, 로그인이 만료됐을 때는 어떻게 다시 이어 가는지 응답에 적혀 옵니다.
- 실험 페이지 맨 끝에 '실행 기록'이 생겼습니다. 결과를 읽는 데 영향을 주는 실패는 본문에, 경로 오타나 설치 문제 같은 작업 중 문제는 실행 기록에 한 줄씩 남깁니다.
- 문헌 페이지에 '읽은 범위'(원문 전체 · 초록만 · 2차 자료)가 생겼고, 작성자 옆에 "초록만 읽고 정리"처럼 보입니다.
- 수식의 기호 설명이 `x_{t}`와 `x_t`처럼 괄호만 다르게 쓴 기호도 찾고, 못 찾으면 수식에 실제로 적힌 형태를 알려 줍니다.

## 0.49.0 — 2026-10-15

Each question now shows where it stands in its research loop (question, prediction, experiment, result, meaning, next move) on the briefing, the flow and the question page, with how long a result has waited. Experiments carry a prediction and decision rule written before they run, and results are read against it. One form records what a result means, revises the answer and starts the next experiment or question; an AI does the same with record_result_meaning. Chip and tree labels read cleanly on standard-density screens.

- 질문마다 지금 루프의 어디에 있는지(질문 · 예측 · 실험 · 결과 · 해석 · 다음 수) 브리핑, 연구 흐름, 질문 페이지에 보입니다. 결과가 나온 지 며칠 됐는지, 실험이 며칠째인지도 함께 나옵니다.
- 실험 페이지에 '예측과 판단 기준'을 적습니다. 실행 전인 실험만 적기를 권하고, 결과가 나오면 예측 옆에 결과가 놓여 "예측대로 · 예측과 다름 · 판단 보류"로 읽힙니다.
- **해석 기록** 한 번으로 예측과의 비교, 이 결과가 질문에 말해 주는 것, 지금까지의 답과 남은 의문, 다음 수(다음 실험 · 새 질문 · 답 정리 · 보류 · 폐기)를 남깁니다. 다음 실험을 고르면 예측까지 적은 실험이 바로 만들어집니다.
- 결과 페이지에 핵심 결론이 없으면 해석의 첫 문장이 핵심 결론이 됩니다. 실행 전 실험에는 결론 대신 예측을 먼저 묻습니다.
- AI도 record_result_meaning 한 번으로 같은 일을 하고, 연구 브리핑에서 해석을 기다리는 결과를 알게 됩니다.
- 칩 글자를 13px 보통 굵기로, 연구 트리의 작은 라벨을 12px로 바꿔 일반 해상도 모니터에서도 "활성" 같은 글자가 뭉치지 않습니다.

## 0.48.0 — 2026-10-15

Invitation links explain themselves before sign-in: the project, who invited you and as what, and the address, already filled in; joining lands you in the project. A Semi-Owner's AI now works without the owner's approval. A teammate's new records gather into one notice per project. A question stays open until an answer from records arrives, and an AI learns of its queued requests when a session starts. Tool results no longer repeat the AI's identity. Account deletion can be requested from Settings.

- 초대 링크를 열면 로그인하기 전에 어느 프로젝트에 누가 어떤 역할로 초대했는지, 그 역할로 무엇을 할 수 있는지, 초대한 사람의 메모와 초대받은 주소가 보입니다. 주소는 미리 채워져 있고, 가입하거나 로그인하면 바로 그 프로젝트로 들어갑니다.
- 다른 계정으로 로그인한 채 초대 링크를 열면 두 주소를 알려 주고, 맞는 계정으로 바꿔 들어갈 수 있습니다.
- 초대하는 쪽은 역할마다 할 수 있는 일을 보고 고른 뒤, 링크를 복사하거나 내 메일로 바로 보냅니다. 초대 목록에는 보낸 날이 나오고, 기한이 지난 초대는 새 링크로 다시 보낼 수 있습니다.
- Semi-Owner가 연결한 AI는 소유자의 승인 없이 프로젝트에서 일합니다. 역할이 Editor나 Viewer로 바뀌면 다시 승인을 받아야 합니다.
- 팀원의 새 기록 알림이 기록마다 오지 않고 프로젝트마다 하나로 모입니다("Attention sink 재현 외 6개"). 누르면 최근 추가에서 새로 들어온 기록에 점이 찍혀 있고, 기록마다 누가 추가했는지 보입니다.
- 내게 온 질문에 내 AI가 기록에서 답을 찾지 못해 "모른다"고만 답하면, 그 질문은 답한 것으로 치지 않고 나에게 그대로 남습니다.
- AI가 세션을 시작할 때 자기에게 맡겨진 AI 작업 요청이 있는지 알게 됩니다.
- AI 도구 응답마다 반복되던 연결 정보를 뺐습니다. AI가 같은 일을 하면서 토큰을 덜 씁니다.
- 개인 설정에 계정 삭제가 생겼습니다. 지워지는 것과 남는 것을 확인하고, 모든 프로젝트를 내보낸 뒤 삭제 요청 메일을 쓸 수 있습니다.

## 0.47.0 — 2026-10-15

Explainers now live inside decks: a slide carries a page's explainer as its own element, live while presenting, where a click or the presenter's keys walk its steps before the slide moves on, and exported to PPTX as a picture beside its steps. The studio's Page figures inserts any explainer, equation or chart from a saved page as a new slide. Clicking a part of an explainer opens the step about it; clicking elsewhere takes the next step. The privacy policy and terms of service are published in English and Korean and linked from sign-up and the AI connection screens.

- 발표 자료에 도해를 넣을 수 있습니다. 발표하는 동안에도 도해가 살아 있어서, 그림을 누르거나 → 키를 누르면 단계가 넘어가고 마지막 단계 다음에 슬라이드가 넘어갑니다. PPTX에는 그림과 단계 목록이 나란히 들어갑니다.
- 발표 편집 화면의 **페이지 그림**에서 저장된 페이지의 도해, 수식, 차트를 골라 새 슬라이드로 넣습니다.
- 도해에서 부분을 누르면 그 부분을 다루는 단계로 바로 갑니다. 빈 곳을 누르면 다음 단계로 넘어갑니다. 부분에 마우스를 올리면 몇 단계에서 다루는지 알려 줍니다.
- 개인정보처리방침과 이용약관을 한국어와 영어로 공개했습니다. 첫 화면 맨 아래, 가입 화면, AI 연결 화면에서 열 수 있습니다.
- 발표 편집 화면의 슬라이드 목록에서 수식이 크게 깨져 보이던 문제를 고쳤습니다.

## 0.46.3 — 2026-10-15

The sign-in consent page and the AI guide carry the site's security headers again, so no other site can frame them. A chart focus shows a tiny change (1e-5 → 2e-5) as the change it is instead of ±0, a to-do keeps the priority a person chose over the title's !, and ⌘K over a page returns to that page when search closes. Explainers are shown whole, and slide text is never cut: story decks measure each box as the slide draws it, and words longer than their box are set smaller, on screen and in PPTX.

- 로그인 동의 화면(/oauth/consent)과 AI 연결 안내(/guide/ai)에 빠져 있던 보안 헤더를 붙였습니다. 다른 사이트가 이 화면을 자기 안에 넣어 보여 줄 수 없습니다.
- 그림의 강조 지점이 아주 작은 변화(1e-5 → 2e-5)를 ±0으로 보여 주던 문제를 고쳤습니다. 변화는 셀에 적힌 자릿수와 표기 그대로(+1e-5, +0.00001) 나옵니다.
- 할 일 제목에 `!`를 넣고 우선순위를 직접 고르면, 고른 값(보통 포함)으로 등록됩니다. 고르기 전에는 우선순위 칸이 제목의 `!`를 따라 보여 줍니다.
- 페이지를 연 채 ⌘K로 검색을 열었다 닫으면 보던 페이지로 돌아갑니다. 한글 입력 상태에서도 ⌘K · ⌘J · ⌘S가 듣습니다.
- 도해 안에 스크롤이 생기지 않고 그림이 통째로 보입니다. 아래쪽 부품의 설명은 부품 위에 뜹니다.
- 발표 슬라이드의 글이 상자에서 잘리지 않습니다. 연구 흐름으로 만든 초안은 슬라이드와 같은 규칙으로 상자 높이를 재고, 이미 만든 발표에서 상자보다 긴 글은 작게 그립니다. 편집 화면에 몇 pt로 줄였는지 나오고 PPTX도 같은 크기로 나갑니다.

## 0.46.2 — 2026-10-14

The research serif's smallest slices now ship as font files. The production build had inlined three of them as data URLs, which the site's content security policy refuses, so a few rare Hangul syllables and CJK brackets were drawn in a fallback face. A build check now fails if a font is ever inlined again.

- 마루 부리 글꼴의 아주 작은 조각 세 개가 사이트 보안 정책(CSP)에 막혀, 드문 한글 음절과 괄호 기호 몇 개가 다른 글꼴로 보이던 문제를 고쳤습니다. 글꼴은 이제 언제나 파일로 내보내고, 빌드가 이를 검사합니다.

## 0.46.1 — 2026-10-14

Type is set in four weights and one size scale with a single name per size, and the research serif is asked only for the two faces it ships, so what the stylesheets say is what readers see. On every screen a deck now speaks the app's faces, Pretendard and the research serif, instead of a portable face with no Hangul, including on a phone, in a zoomed figure and inside an interactive scene. The type rules are written into the design principles that coding agents read first.

- 글자 굵기를 네 단계(400 · 500 · 600 · 700)로 정리했습니다. 그 사이 굵기(450 · 550 · 650)가 사라져 제목 · 라벨 · 본문의 차이가 분명해집니다.
- 마루 부리는 내려받는 두 굵기(400 · 600)로만 씁니다. 연구의 말과 도구의 말이 나뉘는 곳은 한 파일에만 있고, 기록 제목은 고칠 때도 읽을 때와 같은 글꼴 · 크기로 보입니다.
- 발표를 휴대폰으로 보거나, 그림을 확대하거나, 인터랙티브 장면을 열 때도 한글과 영문이 같은 글꼴로 나옵니다.
- 글자 크기 이름이 하나로 통일됐고, 디자인 원칙에 글자 절(두 목소리 · 크기 · 굵기 · 예외)이 생겼습니다.

## 0.46.0 — 2026-10-14

The website now runs on Cloudflare Workers at airesearchloop.com, deployed from the release tag, with the old address kept during the move. Notifications open on the category the red dot announced. To-dos are written as an outline, a goal with its sub-tasks, and every goal opens with its rows. Explainers step when the drawing is clicked and route links around the parts they skip; marks in figures use the accent and say why on hover, and a chart focus carries a one-sentence focusNote. The research voice is set in MaruBuri.

- 웹사이트가 airesearchloop.com으로 옮겨 Cloudflare Workers에서 돕니다. 릴리스 태그를 올리면 사이트가 배포되고 새 버전이 떴는지 확인까지 합니다(`npm run check:site`). 옮기는 동안 예전 chatgpt.site 주소도 함께 열리고, ChatGPT 안의 작업 공간은 새 주소를 쓰는 `workspace-v9`로 바뀌었습니다.
- 알림은 새 알림 · 응답 필요 · 변경 요청 · 팀 진행으로 나뉘어, 빨간 점이 알린 것이 있는 곳으로 바로 열립니다. 읽지 않은 알림이 먼저 오고, 한 줄은 종류 · 제목 · 프로젝트와 시각 순으로 읽힙니다.
- 할 일은 개요처럼 적습니다. 큰 할 일 아래 하위 할 일이 들여 쓰이고, 줄마다 완료 기준이 제목 옆에 있습니다. Enter로 다음 줄, Alt+→/←로 하위·큰 할 일, ⌘/Ctrl+Enter로 등록하고, 담당 · 일정은 제목의 `@이름 ~날짜 !`나 줄 옆의 담당 · 일정에서 정합니다. 목록의 큰 할 일은 하위 할 일을 펼친 채 열리고, 그 끝줄에서 바로 다음 하위 할 일을 더합니다.
- 설명 그림은 그림을 누르면 다음 단계로 넘어가고, 건너뛰는 연결은 부품 옆으로 돌아가며 이름표가 상자에 가려지지 않습니다. 수식은 유도 줄을 누르면 그 줄로 가고, 작은 기호도 넓게 집힙니다.
- 그림 · 표의 강조는 노란색 대신 강조색으로 그리고, 마우스를 올리면 이유를 말합니다. 그림의 강조 지점은 작성자가 남긴 이유(`focusNote`)와 직전 값 대비 변화를, 표의 칠한 값은 어느 열·행에서 무엇보다 좋은지를 보여 주고, 표 아래에 칠한 값의 뜻이 한 줄 붙습니다.
- 질문 · 답 · 제목처럼 연구가 말하는 문장은 마루 부리로 바뀌었습니다. 화면 글자는 Pretendard 그대로입니다.
- 열어 둔 메뉴(발표의 AI에게 요청, 페이지 도구, 노트 도구)가 화면이 뒤에서 다시 그려질 때 저절로 닫히지 않습니다. 쉬는 틈에 다른 화면의 코드를 받아 와도 지금 화면은 다시 그리지 않습니다.

## 0.45.0 — 2026-10-14

One version for the website, the MCP server, the panels and the plugin, released with one command. The Research Loop panel now opens in Claude (claude.ai, Claude Desktop, Claude iOS) through a custom connector as well as in ChatGPT, names the host it runs in, and the connection guides say where the one server address goes.

- 버전이 하나로 합쳐졌습니다. 이전의 MCP 0.44.0 · 플러그인 0.34.0 · 패널 UI 3.1.0/2.4.0이 모두 0.45.0이 되고, 이후로는 `package.json`의 번호 하나만 올립니다.
- Claude 앱에서 패널이 열립니다. 서버가 접속한 호스트를 보고 Claude에는 Claude의 샌드박스 도메인에서 도는 자체 완결형 패널을, ChatGPT에는 웹사이트가 내장된 작업 공간을 내보냅니다. 패널의 문구는 실제 호스트 이름(Claude, ChatGPT)을 씁니다.
- 연결 안내(내 AI, `/guide/ai`, 플러그인 스킬)에 Claude 웹·데스크톱·iOS 항목이 생겼고, 스킬은 패널을 "ChatGPT 전용"이라 부르지 않습니다.
- 첫 프로젝트의 브리핑이 다음 할 일로 AI 연결을 권하고, 할 일 페이지의 추가 줄은 한 줄로 쉬다가 쓸 때 펼쳐집니다. 발표 초안의 슬라이드는 내용에 따라 구성이 달라지고, 드물게 먼저 여는 화면의 코드는 처음 열 때 내려받습니다.

## 0.34.0 — 2026-10-13

Pages carry equations as data: TeX as the paper writes it, each symbol's name, the derivation line by line and variables to move. The app typesets the block, lights a symbol and its name together, walks the derivation and recomputes a value as a variable moves.

- 작성 가이드에 `equation` 모듈이 생겼고, 식 한 줄만 있는 문단은 저장 시 수식 블록으로 옮기라는 안내와 함께 거부됩니다.
- MCP 0.44.0 · 패널 UI 2.4.0과 함께 나왔습니다.

## 0.33.0 — 2026-10-13

The redesigned Research Loop: a briefing on every project, records that lead with their bottom line, tables read as charts and methods drawn as step-by-step explainers from AI-written intent, four Claude Code commands and a linked-repository file.

## 0.31.0 — 2026-10-07

Selected research evidence workspace: a sentence or plot selection prepares a bounded source draft, and only checked evidence enters a team draft.

## 0.30.0 — 2026-10-01

Presentation authoring and PowerPoint guidance.

## 0.29.0 — 2026-10-01

The full website workspace inside ChatGPT, with the human's separate sign-in and permissions.

## 0.28.0 — 2026-10-01

Presentation visual quality guidance and profiles.

## 0.27.0 — 2026-10-01

Presentation references and fullscreen guidance.

## 0.26.1 — 2026-10-01

Fix the Main and Sub to-do hierarchy.

## 0.26.0 — 2026-10-01

Mobile workspace and public review metadata.

## 0.25.0 — 2026-09-30

Native planning and AI coordination.

## 0.24.0 — 2026-09-30

Research workspace and saved-page presentations.

이전 버전의 내용은 플러그인 저장소의 커밋 기록과 앱 저장소의 `docs/plugin-extensions.md`에 있습니다.
