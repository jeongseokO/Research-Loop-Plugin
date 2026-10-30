# 변경 내역

Research Loop는 버전이 하나입니다. 웹사이트, MCP 서버, ChatGPT·Claude 안의 패널, 이 플러그인 패키지가 같은 번호를 씁니다. 새 버전은 맨 위에 `## x.y.z` 항목으로 적습니다. 항목의 첫 문단은 플러그인 디렉터리에 올라가는 release note이므로 영어 한 문단으로 쓰고, 그 아래에 사람이 읽을 내용을 한국어로 적습니다. 릴리스 명령이 제목에 날짜를 붙입니다.

## 0.98.1 — 2026-10-30

Research Loop costs an AI less on every call. The tool list it carries every turn is a fifth smaller (3,992 to 3,187 tokens for Claude): two tools most turns never use now sit one describe_tools call away, and sentences said elsewhere left the descriptions. The project's work instructions come once, from get_project_instructions; other reads say which revision is current instead of repeating the text (286 tokens saved per read for a 485-character instruction). who_am_i says each rule and each role's capabilities once (591 to 379 tokens). Nothing in the database changes.

- 매 걸음 도구 목록: Claude 기준 17,688자(3,992토큰)에서 14,055자(3,187토큰)로, ChatGPT 기준 17,894자에서 14,261자로 줄었습니다(20%). `record_result_meaning`은 `questions` 그룹으로, `report_implementation`은 `projects` 그룹으로 갔습니다. `describe_tools`의 목차가 두 이름을 매번 보이고, 접속 지침의 마무리 줄이 두 도구를 부릅니다(`results: record_result_meaning; code/runs: report_implementation first`). `archive_project`는 남습니다. 호스트는 목록에 있는 파괴적 도구를 그 이름으로 부를 때만 사용자에게 확인을 받습니다.
- 겹치는 문장: 어느 쓰기 전에 어느 지침을 읽는지, 글쓰기 원칙, 지침을 언제 읽는지는 접속 지침이 한 번 말하므로 `get_research_page`, `patch_research_page`, `save_research_page`, `get_guide`, `call_tool_*`, 패널 도구의 설명에서 뺐습니다. 목록 스키마는 0이라는 하한과 1,000자 이상의 상한을 싣지 않습니다. 모든 호출은 지금처럼 엄격한 스키마로 검사하므로, 같은 값은 같은 필드 이름과 함께 거절됩니다.
- 작업 지침: 전문은 `get_project_instructions`만 줍니다. 다른 읽기는 `projectInstructions: {revision, textFrom: "get_project_instructions"}`만 싣고, 지침이 비었으면 `{revision, text: ""}`입니다. 연구 내용 안에 같은 이름의 키가 있어도 건드리지 않습니다. 이력 읽기(`get_project_context`, `sync_project`)는 지침을 바꾼 사건 안에 그 글을 그대로 보입니다. 485자 지침이면 보통 세션의 읽기 일곱 번이 5,510토큰에서 3,508토큰으로 줄었습니다.
- `who_am_i`: 고정 문장은 다른 곳에 없는 두 규칙(충돌의 뜻과 다시 쓰기, 여러 기록과 페이지 요약을 한 번에 쓰는 도구)만 남았습니다. 권한은 역할마다 한 번(`capabilitiesByRole`)이고, 역할과 권한이 다른 프로젝트만 자기 `capabilities`를 지닙니다. 프로젝트 색과 빈 설명은 싣지 않고, API 키의 범위와 만료는 `authentication`에 한 번만 있습니다. 프로젝트 하나일 때 591토큰에서 379토큰입니다.
- 플러그인: 스킬과 `record`, `task` 명령이 옮긴 도구 옆에 그룹을 적습니다.
- 대가: 옮긴 도구를 쓰는 작업은 `describe_tools`로 한 차례를 더 씁니다(답 428토큰과 290토큰). 참조 과제 11개를 그 차례까지 넣어 다시 돌리면 모두 합쳐 모델에게 보낸 글자가 9.4% 줄었고, 옮긴 도구를 쓰는 세 과제는 6–11% 늘었습니다. 세션이 길수록 더 줄어듭니다.
- 배포: 마이그레이션은 없습니다. 함수 `research-loop-mcp`와 `v0.98.1` 태그를 올립니다.

## 0.98.0 — 2026-10-30

An equation can now draw its graph. A curve compares up to four cases along one variable, marks where the reader stands, draws the slope there and says whether the value rises or falls; a 3D surface turns under a drag or the arrow keys; level lines show constraint regions with the lowest point in each, so Lasso's corner lands exactly on zero where Ridge's circle does not. The sliders move every plot on a page and while presenting, and PPTX keeps it as a picture. This release has a database migration.

- 그래프: 값 막대가 있는 수식 블록에 `plot`을 붙이면 세 가지 중 하나를 그립니다. 곡선(변수 하나를 따라 식 1–4개), 3D 곡면(변수 둘의 함수), 등고선과 제약 영역(위에서 본 같은 함수와 영역 1–3개, 영역은 식 ≤ 0인 곳)입니다. 축에 두지 않은 변수는 그대로 값 막대로 남아 그림의 모양을 바꿉니다. 식에 `sign`이 생겼습니다(0–1 손실).
- 곡선: 1, 2, 5 단위 눈금과 축 이름, 계열마다의 색과 지금 값을 적은 범례가 있습니다. 지금 자리에 세로선과 점을 두고, 첫 계열에는 접선을 점선으로 긋습니다. 가로축 위 띠가 늘어나는 구간, 줄어드는 구간, 그대로인 구간을 나누고, 결과 아래에 “y = 1: p 값이 커지면 ↘ 감소 (기울기 -3.333)”처럼 말합니다. −log p처럼 끝없이 커지는 값은 적은 곳에서 자르고, 곡선을 누르거나 끌면 그 자리로 값 막대가 옮겨 갑니다.
- 3D 곡면: 3D 라이브러리 없이 앱이 32×32 격자를 돌려 SVG로 칠합니다. 높이에 따라 옅은 초록에서 짙은 초록으로 칠하고, 지금 점을 지나는 두 단면을 굵게 그어 이름(“p만 바꿀 때”)을 붙입니다. 끌면 돌고(손가락은 가로로만, 세로는 페이지 스크롤), 화살표 키는 좌우로 15°씩 돌리고 위아래로 10°씩 기울이며, Home이나 두 번 누르기로 처음 각도로 돌아옵니다. 결과 아래에 두 변수의 기울기를 함께 말합니다.
- 등고선과 제약 영역: 등고선 10줄(낮을수록 진하게)과 지금 점, 영역마다 옅은 칠과 테두리를 그립니다. 영역 안의 최솟값을 좌표와 함께 찍고(“Lasso 최솟값 (0, 1)”), 전체 최솟값은 속이 빈 점입니다. 축 위로 옮겨도 영역 안이고 값이 커지지 않는 최솟값은 정확히 축에 붙으므로, Lasso의 마름모는 꼭짓점에서 한 가중치가 정확히 0이 되고 Ridge의 원은 두 가중치가 모두 0이 아닌 접점에서 만납니다. 누르면 그 자리로 두 값이 옮겨 가고, 휴대폰에서는 범례가 위로 가고 정사각이 카드 폭을 씁니다.
- 함께 움직이기: 값 막대를 움직이면 그래프, 결과, 계산식, 기울기 문장이 다음 프레임에 함께 바뀝니다. 그래프마다 화면 낭독기가 읽는 요약이 있고, 기울기 문장은 바뀔 때 읽힙니다. 그리스 문자 이름의 변수(`lam`, `alpha`)는 값 막대, 축, 단면, 문장, 계산식에서 λ, α로 보입니다.
- 슬라이드: 넓은 수식 무대에서는 그래프가 식과 유도 아래에 칸의 폭으로, 좁은 무대에서는 값 아래에 무대 폭으로 놓입니다. 자리가 모자라면 캡션과 기호의 뜻이 먼저 빠지고, 그래프는 값 막대 바로 앞에 빠집니다. 글자를 캡션 크기로 쓰고도 읽을 만한 그림이 남지 않으면 그리지 않습니다. 발표 중에는 값 막대가 그래프를 다시 그리고, 곡면은 끌거나 그 위의 화살표 키로 돌며 슬라이드는 넘어가지 않습니다.
- PPTX: 그래프는 SVG 그림 하나(PowerPoint가 쓰는 PNG 미리보기와 함께)로 들어가고, 그림의 설명과 노트에 요약(“예측 확률 p에 따른 손실. p = 0.3일 때 y = 1: 1.204, …”)이 붙습니다. 자리가 없어 그리지 못한 슬라이드도 노트에는 요약이 있습니다.
- AI: 쓰기 지침(개정 53)의 수식 부분이 세 가지를 언제 쓰는지, 계열과 영역은 TeX와 캡션이 말하는 것만 그린다는 것, 끝없이 커지는 값만 자른다는 것을 가르칩니다. 예시 수식에 곡선이 붙었습니다. 수식 부분은 5,770자(전 4,822자, 한도 6,000자)입니다. 저장할 때 잘못은 키를 짚어 돌려줍니다(`plot.y must differ from plot.x.` 등).
- DB: 마이그레이션 `20261030100000_equation_plot.sql`이 수식 블록이 받는 키에 `plot`을 더하고 모양(종류, 그 종류의 키, 블록의 변수인 축, 계열·영역의 수와 글자, 순서대로 된 축 끝)을 검사합니다. 다른 검사는 그대로입니다.
- 데모: 데모 프로젝트에 ‘공부 노트: 손실과 정규화를 그래프로’가 있습니다. 교차 엔트로피, 힌지·로지스틱·0–1 손실, 베르누이 KL 곡면, Lasso와 Ridge의 등고선, λ에 따라 줄어드는 계수(Lasso만 0에 닿음)를 담았습니다. 방법 페이지의 층별 예산 규칙과 데모 논문의 식 (2) 도구에도 곡선이 있습니다.
- 문구: 새 문구 14개를 영어, 일본어, 프랑스어로 옮겼습니다.
- 크기: 첫 화면의 스크립트와 작업 공간은 그대로입니다. 그래프 코드(15.0KB)는 페이지에 그래프가 있을 때만 받고, 슬라이드는 그리는 코드와 함께 받습니다(12.3KB). 그래프 스타일 0.7KB는 앱의 스타일시트에 있어 카드가 미리 자리를 잡습니다. 데모 노트(3.0KB)는 데모에서만 받습니다.
- 배포: 마이그레이션을 먼저 적용하고, 함수 `research-loop-mcp`와 `shared-page`, 그리고 `v0.98.0` 태그를 올립니다.

## 0.97.0 — 2026-10-29

A paper reading can now carry a plain explanation under its abstract and each paragraph: what it says in plain words, one example from the paper's own numbers, and what it is there for, in the reader's language. All of them together are about as long as the paper, so the AI asks before writing them and adds them only on a yes; an existing reading asks for them from View. They switch on and off like the other layers. The demo paper has one under its abstract and every summarized paragraph.

- 쉬운 설명: 초록과 본문 문단(40낱말 이상)마다, 처음 읽는 사람도 따라오게 그 문단이 하는 말을 쉬운 말로 풀고, 예시 하나(논문의 숫자를 직접 넣어 보거나 지어낸 예라고 밝힌 작은 경우)와 이 논문에서 왜 그 말을 하는지를 짧은 문장 2–4개로 씁니다. 그 문단 바로 아래의 옅은 상자에 놓이고, 읽는 사람의 언어로 씁니다.
- 먼저 묻기: 다 달면 읽을 글이 두 배쯤 늘고 시간이 더 들어서, AI가 원문 읽기를 만들기 전에 문단마다 쉬운 설명도 달지 한 번 묻고 그렇다고 할 때만 답니다. 요청에 이미 있으면 묻지 않습니다. 새 원문 읽기 요청 글은 이것을 말하지 않고, 어려운 대목의 풀이는 이제 “예시를 곁들인 설명”이라고 부탁합니다(‘쉬운 설명’은 새 층의 이름).
- 보기: 문단 요약 아래에 ‘쉬운 설명’ 줄(문단마다 예시와 함께, 개수, 스위치)이 있습니다. 끄면 다시 그리지 않고 바로 숨고, 고른 것은 이 기기에 남습니다. 없거나 일부만 있으면 그 줄의 ‘AI에게 맡기기’가 쉬운 설명만 부탁하고, 이 요청에는 AI가 다시 묻지 않습니다. PDF 사본에 쉬운 설명이 있으면 ‘이어서 만들기’가 다음 쪽에도 달라고 합니다.
- AI: `save_paper_glosses`가 `plain_explanations`를 받습니다(사람이 그렇다고 했을 때만이라는 설명과 함께, 한 번에 60개, 언어마다 1,000개, 600자). 결과가 몇 문단에 달렸는지 말하고, `get_paper_reading`은 쪽마다 쉬운 설명이 있는 블록을 알려 줍니다. 읽기 안내는 4,441자(전 3,799자), papers 도구 설명은 10,743자(전 10,290자)입니다. 늘 받는 도구 목록은 그대로입니다.
- 크기 검사: 서버가 풀이의 크기를 DB와 같은 방식(jsonb 글, 쌍점과 쉼표 뒤의 빈칸까지)으로 잽니다. 1 MiB를 넘는 쓰기는 DB의 오류 대신 서버가 이유와 함께 거절합니다.
- 데모: 데모 논문의 초록과 요약이 있는 13문단에 한국어 쉬운 설명이 있습니다. PDF 사본에는 없어서 보기에서 부탁하는 길을 볼 수 있습니다.
- 문구: 새 문구 5개와 바뀐 요청 2개를 영어, 일본어, 프랑스어로 옮겼습니다.
- 크기: 첫 화면은 그대로이고, 읽기 화면이 0.3KB, 작업 공간이 0.2KB 늘었습니다. 데모의 쉬운 설명 14개(2.6KB)는 데모에서만 받습니다.
- 배포: DB 변경이 없습니다. 함수 `research-loop-mcp`와 `shared-page`, 그리고 `v0.97.0` 태그.

## 0.96.1 — 2026-10-29

In ChatGPT and other AI clients, the full workspace hands work to the conversation as you submit it: a task handed to AI, or a question on a reading memo, starts there without a second request. The workspace fills the host's height, keeps the site's index beside record pages and opens a saved memo over a narrow reader without moving the text. The basket and page sharing work in the plugin as on the site. A paper reading's explanations now come in plain words with a worked example.

- 대화로 이어지는 맡긴 작업: AI 클라이언트 안의 작업 공간에서 `AI에게 맡기기`로 작업을 저장하거나 논문 메모에서 `AI에게 묻기`를 누르면, 저장한 요청이 지금 대화로도 갑니다. 요청을 다시 쓰지 않아도 AI가 시작합니다. 이 기기에서 방금 제출한 것만 보내고(불러오기, 새로고침, 다른 기기의 작업은 보내지 않음), 제출이 끝난 뒤 계정과 프로젝트, 저장하지 않은 편집을 다시 확인합니다. 작업은 그 작업을 읽고 확인해 가져간 뒤 시작하라고, 메모는 그 질문과 구절에 답해 그 메모에 저장하라고 정확한 대상을 적어 보냅니다. 대화에는 사람이 보낸 말로 보이므로 그 사람의 언어로 시작합니다(“방금 맡긴 작업을 시작해 주세요.”). 자동으로 다시 보내지 않습니다.
- 사이트와 같은 기능: 플러그인에서도 바구니와 페이지 공유(Owner와 Semi-Owner의 `공유`, 공유받은 페이지)를 씁니다. 바구니는 그 창의 브라우저 저장소에 있어서 사이트의 바구니와는 따로입니다. 로그인이 따로인 것과 같습니다.
- 화면: 호스트가 주는 높이를 다 씁니다(높이를 주지 않을 때만 760px, 좁은 화면 720px). 기록 페이지 옆에 사이트처럼 색인이 남고, 위쪽 한 줄에 공간 전환과 AI 입구가 있습니다. 그림의 두 동작(팀 초안에 담기, AI에게 맡기기)은 그림 가장자리의 아이콘입니다. 고른 글 옆의 메뉴는 글에서 8px 떨어져 뜨고, 아래에 자리가 없으면 위에 뜨며, 읽는 자리가 움직이면 닫힙니다.
- 좁은 화면의 메모와 돌아오기: 저장한 메모는 떠 있는 카드(휴대폰은 아래에서 올라오는 시트)로 열려 아래 문단이 밀리지 않습니다. 팀 공간에서 돌아오면 스크롤을 그대로 되살리고, 폭이 바뀌어 글이 다시 흘렀으면 고른 부분이 보이게 합니다.
- 말: 작업 공간은 ChatGPT, Codex 등 사이트를 띄우는 어느 호스트에서나 열리므로 한 호스트의 이름을 쓰지 않습니다(`AI에게 맡기기`, `AI와 다듬기`, 계정과 권한 안내). 요청 창 아래에는 “대화의 AI에게 바로 보냅니다. 맡긴 작업 목록에는 남지 않습니다.”가 있고, 요청을 준비만 하는 사이트의 요청 창은 ChatGPT와 Claude를 함께 안내합니다.
- 메모의 질문: AI 클라이언트 안에서 메모로 물은 질문은 이미 대화로 갔으므로, 카드에는 “이 대화의 AI가 답하면 여기에 달립니다.”라고만 씁니다. 데모의 안내는 “실제 작업 공간에서는 연결한 AI의 답이 여기에 달립니다.”입니다.
- 논문 설명: 논문 읽기의 어려운 대목에 다는 설명을, 쉬운 말로 뜻을 말하고 작은 예시(논문의 숫자를 직접 대입해 보기, 아주 작은 경우, 항 하나가 커지면 어떻게 되는지)로 보여 준 뒤 왜 중요한지까지 2–5문장으로 쓰게 했습니다(AI가 논문 읽기 전에 읽는 지침). 낱말 뜻의 보충 설명에는 한 줄 예시를 붙입니다. 앱이 보내는 논문 읽기 요청도 “어려운 대목에는 예시를 곁들인 쉬운 설명을”로 바뀌었고, 데모 논문의 설명 다섯 곳이 그 모양입니다.
- 크기: 첫 화면은 그대로이고 작업 공간이 0.4KB, 읽기 화면이 0.7KB 늘었습니다. 대화로 보내는 부분(1.1KB)은 플러그인에서만 받습니다.
- 배포: DB 변경이 없습니다. 함수 `research-loop-mcp`와 `shared-page`, 그리고 `v0.96.1` 태그만 올립니다(0.96.0이 함께 들어 있습니다).

## 0.96.0 — 2026-10-29

Slides speak in points. A page or story deck turns each paragraph in a list, a reading or a closing slot into one point per sentence; in Korean each point ends in 개조식 (회복함, 가설임), and the sentences stay in the speaker notes. Titles stay claims. Points past what a purpose shows on one slide continue evenly on the next. An AI deck keeps the structure its AI chose, ends its Korean words in 개조식 and always opens on a cover. As points, under Whole presentation, turns a saved deck's words into points in one step.

- 항목으로: 목록, 그림 곁의 해석, 수식의 기호 풀이와 조건, 곁 메모, 정리의 결론과 다음 단계, 비교의 양쪽은 문장이 둘 이상인 문단을 문장마다 글머리표 하나로 나눕니다. 한 문장이면 한 줄 그대로입니다. 목록은 번호가 있든 없든 그대로이고, 한 항목 안의 문장들은 끝만 바꿔 `. `로 잇습니다. 부제, 요지, 받침 줄, 요약 줄, 수식 아래 줄, 비교의 판정은 끝만 바꿉니다. 제목, 이름 줄, 큰 수치와 그 메모, 표와 차트, 캡션, 그림, 인용 블록은 쓴 그대로입니다.
- 개조식: 했다·합니다 → 함, 된다·됐다 → 됨, 이다·입니다 → 임, 아니다 → 아님, 값이나 명사 + 다 → 임(81.8%임, 원리임), 받침 + 다 → 음(왔음, 높음), 는다 → 음(바로잡음), ㄴ다 → ㅁ(줌, 모름, 씀), ㅂ니다 → ㅁ(감), ㄹ 받침 → ㄻ(긺). 연구 페이지에 나오는 불규칙(만듦, 어려움, 놀라움, 들음, 지음, 나음, 그러함, 것임)과 동사처럼 보이는 명사(차이임, 길이임, 이하임)를 압니다. 목적어 뒤의 동사 원형과 페이지가 원형으로 쓰는 동사는 ㅁ으로 끝냅니다(학습률을 낮추다 → 낮춤, 시간이 걸리다 → 걸림). 명사는 그대로 명사입니다(세 가지임, 줄이기임). 괄호, 인용 번호, 굵게는 제자리에 남습니다. 물음, 권유와 명령, 해요체, 느낌표, 인용, 영어, 조사로 끝나는 조각(토큰마다)은 쓴 그대로 둡니다. 명사로 끝나는 항목도 마침표를 떼어 한 목록 안의 모양이 같습니다.
- 노트: 끝맺음이 바뀐 칸은 페이지에 쓴 문단을 그 슬라이드의 노트에 한 번 둡니다. 영어를 항목으로 나누기만 했거나 마침표만 뗀 칸은 노트에 다시 쓰지 않고, 노트에 이미 있는 문장도 다시 쓰지 않습니다.
- 이어지는 항목: 한 장에 보이는 항목 수는 용도를 따릅니다(학회 발표 4, 저널 클럽 5, 랩 미팅 6, 서면 보고 8). 넘치면 같은 제목으로 다음 장에 이어지고, 장마다 고르게 나눕니다(다섯 개가 한 장에 넷까지 들어가면 넷과 하나가 아니라 셋과 둘).
- AI 덱: AI가 정한 구조는 그대로 두고 한국어 글의 끝만 바꿉니다(나누지 않고, 노트도 그대로). 첫 장은 늘 표지입니다. 뒤에 쓴 표지는 맨 앞으로 오고, 표지가 없으면 결과의 제목으로 하나 더합니다. 검토를 열 때 이름 줄이 빈 표지에 그 사람과 그날을 적어, 검토한 덱과 초안에 넣는 덱이 같습니다. 0.95.0의 계약으로 맡겨 둔 요청도 그대로 검토할 수 있습니다.
- 개조식으로: `발표 전체`의 `말투`에 있습니다. 저장된 덱의 모든 슬라이드를 같은 규칙으로 한 번에 바꾸고(레이아웃 없는 슬라이드는 글 상자의 끝만), 실행 취소 한 번에 모두 돌아옵니다. 상태 줄이 "슬라이드 2장에서 문장 3개를 개조식으로 바꿨습니다."처럼 말하고, 다시 누르면 "바꿀 문장이 없습니다."입니다. 슬라이드를 더하지는 않아서, 칸을 넘치는 항목은 점검에 `다음 슬라이드로 잇기`와 함께 나옵니다.
- 굵은 머리말: 굵은 부분이 있는 글을 통째로 굵게 재던 것을, 글자마다 제 굵기와 굵게 중 넓은 쪽으로 잽니다. 굵은 띄어쓰기가 보통 띄어쓰기보다 좁아서 굵은 머리말 뒤의 긴 줄이 상자를 7px까지 넘을 수 있었습니다(0.95.0부터).
- AI: 발표 지침(개정 52)이 슬라이드의 말을 문장이 아니라 항목으로, 항목 하나에 두 줄까지, 한국어는 명사나 ~함/~임/~됨으로 끝내고 ~다/~습니다는 쓰지 않게 합니다. 제목은 그대로 주장 한 문장이고, 완전한 문장은 노트로 갑니다. 덱 계약에 `slides[0] is the cover`가 들어갔습니다. 지침은 2,997자, 덱 계약과 합쳐 4,389자로 한도(3,000자, 4,400자) 안입니다.
- 문구: 새 문구 6개를 영어, 일본어, 프랑스어로 옮겼습니다.
- 크기: 개조식 규칙(3.3KB)은 덱을 처음 열 때 받는 덱 공용 덩어리에 들어갑니다. 첫 화면은 그대로이고 작업 공간은 0.1KB 늘었습니다.
- 배포: DB 변경이 없습니다. 함수 `research-loop-mcp`와 `shared-page`, 그리고 태그로 사이트와 플러그인.

## 0.95.0 — 2026-10-29

Slides read as designed. Each purpose sets its titles, body and captions on one scale, so a title stands well above its words, and the words beside a figure keep a column away. A page's words keep their bold lead-ins, a page deck never runs over its slides, and a wide picture keeps its height with its caption beside it. An equation sets out its symbols, derivation and values on the slide and answers while you present. A reading names its blurry arXiv figures, and Sharpen from the PDF cuts them again from the paper's PDF.

- 글자 위계: 내용 슬라이드의 제목, 본문, 캡션 크기를 용도가 함께 정합니다. 제목과 본문의 시작 크기(괄호 안은 칸이 모자랄 때 줄어드는 바닥)는 학회 발표 40pt(32)와 24pt(20), 랩 미팅 36(28)과 20(16), 서면 보고 30(24)와 16(13), 저널 클럽 36(28)과 22(18)입니다. 제목은 본문의 1.6배에서 시작하고, 가장 줄어도 본문의 시작 크기보다 25% 이상 큽니다. 데모의 랩 미팅 슬라이드는 제목 32pt와 본문 24pt에서 36pt와 20pt가 됐습니다. 모양은 제목의 굵기와 자리를 그대로 정합니다. 랩 템플릿은 제목 크기를 지키고 본문을 그 3/4 아래에서 시작합니다. 바닥의 쪽 번호, 출처, 챕터는 12pt입니다. 저장된 덱도 새 크기로 다시 흐르고, 사람이 칸에 정한 크기는 그대로입니다.
- 그림과 글 사이: 그림 곁의 해석, 표의 읽는 법, 목록의 곁 메모, 정리의 다음 단계, 수식의 기호 풀이가 그림에서 격자 한 칸 떨어집니다. 긴 해석은 좁은 칸에서 작아지기 전에 넓은 그림 아래로 가서 제 크기를 지킵니다. 그 자리에서 그림이 작아진다면(차트, 보통 비율의 그림) 그림은 곁에 제 크기로 남고 해석이 조금 작아집니다. 정리 슬라이드의 오른쪽 칸에 `다음 단계`라는 이름이 붙습니다.
- 넓은 그림: 칸을 다 채우지 못하는 그림(낮은 칸의 넓은 그림, 세로로 긴 그림)은 칸의 높이를 다 쓰고 캡션이 그 옆에 섭니다. 데모의 넓은 그림이 발표 슬라이드에서 436×147에서 734×248이 됐습니다. PowerPoint도 같습니다.
- 페이지에서 온 글: 굵은 머리말(`**노이즈:**`)이 굵게 남고, 빈 줄은 문단 나눔 하나가 되며, `=`나 `÷` 같은 기호로 줄이 시작하지 않고, 차트의 음수는 `−22`로 씁니다.
- 페이지 덱: 칸을 넘치는 본문은 다음 슬라이드로 이어지고, 그림 곁의 긴 해석은 앞 문장만 남기고 전체를 노트에 둡니다. 서면 보고 덱에 빈 요약 줄이 붙지 않고, 정리의 결론과 불확실함은 목록입니다.
- 수식 무대: 기호, 유도, 값이 있는 수식은 큰 그림 레이아웃에서 식, 번호 붙은 유도와 그 이유, 식에서처럼 그린 기호와 이름, 값 슬라이더와 크게 쓴 결과와 작은 곡선을 함께 펼칩니다. 자리가 모자라면 캡션, 기호의 뜻, 곡선, 계산식, 이유 순으로 물러나고 값은 끝까지 남습니다. 편집기와 PowerPoint에는 유도의 마지막 줄이 보이고, PowerPoint의 글은 고칠 수 있는 텍스트, 식은 그림입니다.
- 발표 중 수식: 슬라이드에 들어서면 유도의 첫 줄이 보이고, Space나 →가 한 줄씩 넘긴 뒤 다음 슬라이드로 갑니다. 기호를 가리키면 식과 유도의 모든 줄에서 그 기호가 밝아지고, 누르면 밝은 채로 남습니다. 값을 움직이면 결과와 곡선이 따라옵니다. 화면 낭독기는 단계와 값을 듣습니다. 휴대폰에서는 페이지의 수식 그림이 그대로 나옵니다.
- 논문 그림 선명하게: arXiv HTML 판의 그림은 100 DPI로 그려져 레티나 화면에서 흐립니다. 읽기 화면이 그림을 보이는 크기로 재어, 그림을 넣을 수 있는 사람에게 머리에 "그림 N개가 흐립니다."와 `PDF로 선명하게`를 보입니다. 누르면 논문 PDF(이 탭에서 연 것, 고른 것, 데모의 것)로 흐린 그림과 빠진 그림을 차례로 다시 자릅니다. 캡션이 분명히 그 그림의 것인 쪽에서만 자르고, 이미 선명한 그림은 두며, 바꾼 그림마다 `되돌리기`, 찾지 못한 그림마다 `직접 고르기`가 있습니다. 사람이나 AI가 넣은 그림은 건드리지 않고, PDF는 이 기기에서만 읽습니다.
- AI: 발표 지침(개정 51)은 기호, 유도, 값이 있는 수식을 `figure`에, 맨 수식만 `equation`에 놓고, 그림 곁의 글은 한두 문장으로 쓰게 합니다. 논문 읽기 지침은 arXiv 사본의 흐린 그림을 `PDF로 선명하게`로 바꿀 수 있다고 사람에게 알리게 합니다.
- 크기: 읽기 화면은 0.7KB(gzip) 늘었고, 선명하게 하는 창(3.4KB)은 처음 누를 때 받습니다. 수식 무대(4.0KB)와 MathJax의 추가분(0.4KB)은 수식이 있는 덱에서만 받습니다. 첫 화면은 그대로입니다.
- 배포: DB 변경이 없습니다. 함수 `research-loop-mcp`와 `shared-page`, 그리고 태그로 사이트와 플러그인.

## 0.94.0 — 2026-10-28

Share one page with people outside your project, the way Google Drive shares a file. An Owner or Semi-Owner opens Share on a page, adds people by email or opens it to anyone with the link, and copies the link or sends it from their own mail app. They read that page alone, view only, with its pictures and files, and nothing else of the project: not its name, its other records or its members. Pages shared with you wait under Shared with me, project settings list every shared page, and an AI reading a page is told whether it is shared. No tool shares a page.

- 공유: 페이지를 읽는 화면의 `편집` 앞에 `공유`가 있습니다. Owner와 Semi-Owner에게, 활성 프로젝트의 공유할 수 있는 페이지에서만 보입니다(할 일, 마감, 토론 노트, 연구 트리 노트는 공유하지 않습니다). 아이콘이 상태를 말합니다: 사람 더하기(아직 아무도), 사람들(추가한 사람), 지구(링크가 있는 누구나). 다른 멤버에게는 머리에 `링크로 공개`나 `3명에게 공유` 칩이, 공유된 페이지를 편집하는 사람에게는 편집기 위에 "저장하면 바로 보입니다" 한 줄이 보입니다.
- 공유 창: 사람 추가(쉼표, 띄어쓰기, 줄바꿈으로 여럿. 한 번에 20명, 한 페이지에 50명. 프로젝트 팀원은 넣지 않고 형식이 틀린 주소는 그 주소를 말합니다), 방금 추가한 사람에게 `메일로 알리기`(내 메일 앱, 여럿이면 숨은 참조), 볼 수 있는 사람과 빼기, `추가한 사람만`(기본)과 `링크가 있는 누구나`, `링크 복사`, `···` 안의 `링크 다시 만들기`와 `공유 중지`. 고르는 대로 바로 저장되고, 실패하면 그 전으로 돌아갑니다. 저장하는 동안에도 키보드가 창 안에 있습니다. 휴대폰에서는 아래에서 올라오고, 창의 코드는 처음 누를 때 내려받습니다.
- 공유된 페이지(`/share#…`): 그 페이지 하나가 프로젝트에서와 같은 모양으로 열립니다. 종류와 상태, 제목, 쓴 사람, 핵심 결론, 속성, 본문과 그림·파일. 프로젝트 이름, 다른 기록, 토론, 변경 이력, 이메일은 서버가 처음부터 보내지 않고, 본문 속 다른 기록의 링크는 작은 자물쇠가 붙은 글자로 남아 열리지 않습니다. 그림 주소는 1시간 가고, 깨지면 1분에 한 번까지 새로 받습니다. 링크 ID는 주소의 `#` 뒤에 있어 서버 기록과 다른 사이트에 남지 않고, 검색 엔진에 실리지 않습니다. 받은 사람의 브라우저 언어로 열리고(고른 언어나 계정 언어가 있으면 그것), 문서처럼 스크롤되며, 인쇄하면 본문만 나옵니다. 작업 공간 묶음을 내려받지 않습니다.
- 받는 사람: `추가한 사람만`이면 그 이메일로 로그인해야 열립니다(확인된 이메일만). 계정이 없으면 같은 주소로 가입하면 되고, 확인 메일의 링크가 열려던 페이지로 돌아옵니다. 다른 계정이면 "이 계정으로는 열 수 없습니다"와 `다른 계정으로 로그인`. 중지한 공유, 바뀐 링크, 휴지통의 페이지, 보관한 프로젝트는 모두 "열 수 없는 링크"입니다. 그 프로젝트의 멤버에게는 `프로젝트에서 열기`가 있습니다.
- 공유받은 페이지: 내 연구 아래에 있고, 하나라도 있을 때만 보이며 아직 열지 않은 수가 붙습니다. 줄마다 종류, 제목, 공유한 사람과 날짜, `새로`. 누르면 새 탭에서 열립니다. 로그인한 채 `/share`만 열어도 같은 목록이 나옵니다.
- 프로젝트 설정: 팀 다음에 `공유 중인 페이지`. 범위, 공유한 사람, 날짜가 보이고, Owner와 Semi-Owner는 줄마다 `공유 설정`으로 공유 창을 엽니다.
- AI: `get_research_page`가 `sharing`(`{ "anyoneWithLink": …, "people": … }`, 공유하지 않았으면 null)을 돌려줍니다. 지침은 공유된 페이지를 고치면 밖에서도 바로 보인다는 것과, 어떤 도구도 페이지를 공유하거나 그 링크를 주지 않는다는 것을 말합니다. Claude와 ChatGPT의 패널에는 공유 단추가 없습니다(칩과 편집 줄은 보입니다).
- 데이터와 보안: 마이그레이션 `20261028200000_page_sharing`이 공유 표 둘과 함수들을 더합니다. 표는 직접 읽거나 쓸 수 없고, 바꾸는 함수는 Owner와 Semi-Owner만 통과하며, 공유된 페이지를 읽는 `rl_read_shared_page`는 서비스 역할만 부릅니다. 새 Edge Function `shared-page`가 링크를 확인하고 보여도 되는 것만 골라, 그 페이지의 첨부만 서명합니다. AI의 OAuth 토큰은 로그인한 사람으로 치지 않습니다.
- 문구: 공유된 페이지의 말은 번역 묶음의 새 `share` 부분에 있어, 공유된 페이지가 작업 공간의 번역을 내려받지 않습니다. 새 문구 79개를 영어, 일본어, 프랑스어로 옮겼습니다.
- 법적 문서: 개인정보 처리방침(공유받는 사람의 이메일, 지우는 때, 누가 무엇을 보나), 이용약관(공유하는 사람의 확인), 개정 공지(10월 28일 추가)에 페이지 공유가 들어갔습니다. 11월 24일 시행을 알린 공지에 나중에 더한 것이라, 다시 공지할지는 소유자가 정합니다.
- 크기: 공유된 페이지는 처음에 스크립트 299.5KB(gzip)를 받습니다(첫 화면은 326.7KB). 그 가운데 공유된 페이지만의 것은 50.0KB이고, 차트 표·설명 그림·수식의 코드(50.6KB)는 그런 그림이 있는 페이지만 받습니다. 처음 만든 빌드는 모든 페이지가 이 코드와 발표 코드를 받아 357.6KB였습니다. 글을 꾸미는 코드(markdown-it과 KaTeX, 133.4KB)는 작업 공간처럼 필요할 때 받습니다. 번역의 `share` 부분은 언어마다 10~11KB, 공유 창은 7.3KB(처음 누를 때), 작업 공간 묶음은 1.8KB 늘었습니다.
- 배포: 마이그레이션 `20261028200000_page_sharing` → 함수 `shared-page`(JWT 검사 없이, `--no-verify-jwt`) → 함수 `research-loop-mcp` → 태그로 사이트와 플러그인. `shared-page`는 사이트와 허용 목록을 함께 쓰므로 이제 릴리스마다 함께 배포합니다(릴리스 명령의 안내와 `docs/release.md`). 사이트가 먼저 올라가면 마이그레이션 전에는 공유 창이 상태를 읽지 못하고, 함수 전에는 공유된 페이지가 "페이지를 불러오지 못했습니다"를 보입니다.

## 0.93.0 — 2026-10-28

Open Research Loop has a team space. What teammates asked of you, the discussions, the work you gave to AI and the people on the project are in one place, in ChatGPT and in Claude, with a count beside its name. In ChatGPT you answer, ask, accept and decline in your own name. In Claude the panel hands each of these to Claude as one request and never writes as you. Claude's panel trades its side index for four places along the top, and ChatGPT's workspace has one bar fewer.

- 팀 공간: ChatGPT 작업 공간과 Claude 패널에 같은 모양, 같은 말로 있습니다. 나에게 온 것(질문, 할 일 요청, 결과 확인, 막힌 작업, 답변), 토론(최근 여섯), 맡긴 작업(넷), 팀원(나부터) 순서입니다. 머리의 `질문하기`나 팀원 줄의 `질문하기`로 세 명까지 묻고, 아무도 고르지 않으면 토론이 됩니다. 구획마다 불러오는 중, 비었음, 실패(다시 불러오기), 찬 상태가 있고, 실패한 뒤에 예전 줄을 보여 주지 않습니다.
- 새로 온 것: 목적지 이름 옆에 나에게 온 것의 수가 붙고(`팀 공간 3`), 새로 생기거나 움직인 줄에 `새로`가 붙습니다. ChatGPT 쪽은 사이트의 안 읽음(`새 답글 2`, `알림 3`), Claude 쪽은 이 기기에서 그 프로젝트의 팀 공간을 마지막으로 본 때가 기준이고, 패널은 읽음을 바꾸지 않습니다. 패널이 닫혀 있을 때는 `who_am_i`가 기다리는 것이 있을 때만 `ownerWaiting` 한 줄을 돌려주어, AI가 대화의 첫 답에서 누가 무엇을 기다리는지 알립니다. 호스트의 플러그인 아이콘 배지나 푸시는 MCP Apps가 앱에 열어 두지 않았습니다.
- ChatGPT 작업 공간: 사람의 사이트 로그인으로 움직입니다. `답하기`는 작업 공간의 그 토론 답변 칸으로 갑니다. `질문하기`는 내 이름으로 올리고 질문받은 사람에게만 알림이 갑니다. `수락`은 바로, `거절`은 같은 줄에서 한 번 더 묻습니다. 이 기기의 공유 초안은 `공유 초안 2`로 팀 공간 안에서 열리고 그리로 돌아옵니다. 보기 권한이면 읽기만 합니다.
- Claude 패널의 팀 공간: 패널의 쓰기는 연결한 AI의 이름으로 기록되므로, 사람 대신 쓰거나 수락·거절하거나 읽음을 바꾸지 않습니다. 동작마다 Claude에 요청 하나(의도, 대상 ID, 사용자가 쓴 말)를 보냅니다. 질문의 `답하기`는 패널 안에서 토론을 열고 끝에 `Claude에 답변 요청`과 `사이트에서 내가 답하기`를 둡니다. 할 일 요청은 `Claude와 살펴보기`와 사이트, 결과 확인은 패널 안의 작업 상세입니다. 연결된 기록은 패널이 읽은 적 있으면 제목으로 보입니다.
- Claude 패널의 틀: 왼쪽 색인 대신 위에 목적지 넷(연구 홈, 연구 기록, 할 일, 팀 공간)이 있습니다. 연구 홈은 나에게 온 것부터, 연구 기록은 검색과 갈래 칩(노트 포함), 할 일은 `목록 | 일정` 전환입니다. 예전 자리(노트, 일정, AI 협업)로 가는 링크는 모두 그대로 열립니다. 목록 폭은 760px입니다.
- ChatGPT의 머리줄: 로그인한 사이트가 틀을 그린다고 알리면 바깥 틀의 머리줄이 사라지고 데스크 줄 하나가 남습니다(`작업 공간 | 팀 공간`, `ChatGPT에 요청`, `···` 안의 최신 내용·밝게·어둡게·사이트 열기, `넓게 보기`). 전체 화면에서는 `작게 보기`로 바뀝니다. 함수와 사이트의 판이 섞여도 넓게 보기와 사이트 열기는 남습니다. `연구 노트` 공간은 `작업 공간`이 되었습니다.
- MCP: 앱 전용 읽기 도구 `get_panel_team`이 팀 공간을 한 번에 채웁니다(팀원 100, 질문 10, 요청 10, 결과 5, 막힘 5, 답변 5, 토론 6, 작업 4, 본문 없이 제목만). 마이그레이션 `owner_task_requester`가 `get_my_research_tasks`의 배정마다 맡긴 사람(`assigned_by_name`)과 시각(`requested_at`)을 더합니다. `open_research_panel`의 설명, 플러그인 스킬의 `references/panel.md`, `docs/MCP.md`가 팀 공간과 패널이 하지 않는 일을 말합니다.
- 크기: Claude 패널 HTML 2,081,970자(0.92.0보다 29,260자, 한도 40,000자). 번들에 남았지만 화면에 나오지 않던 문구 99개(16,190자)를 패널 빌드에서 뺐습니다. ChatGPT 작업 공간 틀은 328자 늘었습니다. 사이트(gzip)는 앱 본체가 0.7KB, 작업 공간 데스크가 스크립트 8.9KB와 스타일 1.9KB, 번역 묶음이 각각 약 1KB 늘었습니다.
- 라이선스: 플러그인 파일(스킬, 명령, 참고 문서, 스크립트, 매니페스트)은 Apache License 2.0을 따릅니다(소유자 결정). 플러그인 폴더와 마켓플레이스 맨 위에 같은 LICENSE가 있고, Claude 매니페스트가 `Apache-2.0`을 밝힙니다. Research Loop의 이름과 로고는 이 라이선스에 들어 있지 않고, 서비스 이용은 이용약관을 따릅니다. 이제 `claude plugin validate --profile directory`가 아무것도 지적하지 않습니다.
- 배포: 마이그레이션 `20261028100000_owner_task_requester` → MCP 함수(`research-loop-mcp`) → 태그로 사이트와 플러그인. 마이그레이션 전에는 할 일 요청이 맡긴 사람 없이 보일 뿐 실패하지 않습니다.

## 0.92.0 — 2026-10-28

Research Loop now sets up properly in Claude. Add the connector at airesearchloop.com/mcp in Claude's Customize → Connectors and it carries Research Loop's own icon; add this marketplace in Customize → Plugins and the plugin's guidance and commands work in chat, in Cowork and, signed in with the same account, in Claude Code. Tools that only read say so, and Claude runs them without asking. Codex and the ChatGPT app keep their connection exactly as it is.

- MCP 주소: `https://airesearchloop.com/mcp`가 같은 MCP 서버입니다. 사이트가 요청을 함수로 넘기고, 답은 흘려보냅니다(SSE 포함, 본문 2 MiB까지, 쿠키는 넘기지 않음). Claude는 커넥터 아이콘을 주소의 도메인에서 가져오므로, 이 주소로 연결하면 Research Loop 아이콘이 보입니다(Supabase 주소는 번개 모양이었습니다). 함수 주소도 그대로 답해서 Codex 플러그인, ChatGPT 앱, 그전의 연결은 바뀌지 않습니다.
- 인증: 서버가 연결한 주소의 메타데이터(`/.well-known/oauth-protected-resource/mcp`)와 401 안내를 돌려주고, 동의 함수가 두 주소를 받습니다(마이그레이션 `mcp_site_resource`). 끝에 `/`가 붙거나 대소문자가 다른 주소는 지금처럼 거절합니다. 토큰은 어느 주소로 연결했든 함수 주소 하나를 대상으로 합니다. 브라우저로 `/mcp`를 열면 연결 안내로 갑니다.
- AI 연결 화면: '연결하기'의 첫 칸이 Claude입니다. 번호 붙은 세 걸음으로 커넥터(주소 복사, Claude의 커넥터 설정 열기, Register automatically), 플러그인(마켓플레이스 복사, 플러그인 설정 열기), 같은 계정의 Claude Code를 안내합니다. 이 화면이 보여 주고 복사하는 MCP 주소가 사이트 주소입니다(Codex·Claude Code 직접 연결 설정 포함). 옛 'Claude 웹, 데스크톱, iOS' 줄은 없어졌습니다.
- 플러그인: Claude가 읽는 `.mcp.json`은 서버 하나, 이름 `research`, 사이트 주소입니다. Claude Code의 도구 이름이 가장 긴 것도 62자로 API의 64자 한도 안에 듭니다(옛 이름으로는 74자). Codex는 매니페스트가 가리키는 `.mcp.codex.json`(서버 이름 `research-loop-plugin`, 함수 주소, OAuth 설정)을 그대로 씁니다. Claude 매니페스트에 표시 이름, Claude에서 하는 일을 말하는 설명, 1024px 아이콘, 문서·개인정보·약관 주소가 있고, 플러그인 폴더에 영어 README가 있습니다. `claude plugin validate --strict`를 플러그인과 마켓플레이스 모두 통과하고, 디렉터리 기준으로는 라이선스만 남았습니다(정하실 일입니다).
- 도구 표시: `get_project_instructions`를 읽기로 표시해 Claude가 묻지 않고 실행합니다(읽은 지침 판의 기록은 연구 내용을 바꾸지 않습니다). `call_tool_write`는 덮어쓰기·지우기를 부르므로 파괴적으로 표시해 Claude가 늘 묻습니다. 제목 셋을 고쳤습니다(Find Research Records, Read the Research Brief, Check Workspace Access). 서버 정보의 아이콘에 사이트의 SVG와 512px PNG를 더했습니다.
- 아이콘: `public/favicon.svg` 하나에서 favicon.ico(16·32·48), apple-touch-icon(180), icon-512.png, 플러그인 목록 아이콘(1024)을 그립니다(`node scripts/build-icons.mjs`). 큰 아이콘은 꽉 찬 바탕이라 플랫폼이 모서리를 둥글려도 표지가 잘리지 않습니다. `/favicon.ico`는 이제 SVG로 넘기지 않고 진짜 ICO를 줍니다.
- 패널: Claude 패널의 `ui.domain`이 연결한 주소에 맞습니다(사이트 주소와 옛 함수 주소 각각).
- 안내: 연결 안내(한국어·영어)가 Claude(웹·데스크톱·모바일·Cowork)로 시작하고, Claude Code 절은 계정으로 따라오는 길과 터미널 길을 함께 적습니다. MCP만 연결하는 주소는 사이트 주소입니다. 문제 해결에 번개 모양 아이콘, 등록 방식, 패널을 더했습니다.
- 라이브 확인: `npm run check:site`가 `/mcp`의 401 안내와 메타데이터의 resource까지 봅니다.
- 다시 연결: Claude 앱의 옛 커넥터(Supabase 주소)는 지우고 사이트 주소로 다시 추가합니다. Claude Code에 플러그인으로 연결해 둔 사람은 서버 이름과 주소가 바뀌어 `/mcp`에서 한 번 다시 인증합니다. 승인 화면의 '연결할 AI'에서 쓰던 AI를 고르면 이름·권한·프로젝트 승인이 이어집니다.
- 배포: 마이그레이션 `20261027233000_mcp_site_resource` → MCP 함수(`research-loop-mcp`) → 태그로 사이트와 플러그인. 이 순서가 아니면 사이트 주소로의 연결이 거절됩니다(동의 함수가 주소를 모르거나, 메타데이터가 함수 주소를 말함). 0.91.0을 아직 올리지 않았다면 이번 배포가 그 내용까지 싣습니다.

## 0.91.0 — 2026-10-27

A paper reading now has layers you switch on and off: the meanings, the notes, the memos, a short summary before each paragraph in your language, and the key sentences the paper rests on, painted like a highlighter. View holds them all, with a sample of how each looks, how many there are and its switch, keeps your choice on the device, and hands summaries or key sentences that are missing to your AI. Your AI writes both when it makes a reading, and the reading guide says what a good summary and a good key sentence are.

- 보기: 읽기 화면 위 줄의 '보기'가 층 다섯을 한 판에 모읍니다. 줄마다 화면에서 보이는 모양 그대로의 견본, 개수, 스위치가 있고, 줄의 글을 눌러도 스위치가 바뀝니다. '모두 끄기'와 '모두 켜기', 풀이 언어 고르기도 이 판에 있습니다(위 줄의 '뜻' 스위치와 언어 고르기는 판으로 옮겼습니다). Esc나 바깥을 누르면 닫히고, 휴대폰에서는 아래에서 올라옵니다. 고른 것은 이 기기에 남고, 처음에는 모두 켜져 있습니다.
- 문단 요약: 본문 문단(40낱말 이상)과 목록마다 그 앞에 한두 문장의 요약이 풀이 언어로 섭니다. 논문 글자보다 작은 고딕에 왼쪽 청록 선이라 원문과 섞이지 않고, 화면 읽기 도구에는 '문단 요약:'이 먼저 들립니다. 부록 문단은 부탁할 때만 요약합니다.
- 핵심 문장: 논문을 떠받치는 문장(질문, 발견, 주된 결과, 한계 같은)을 문헌 색의 옅은 칠로 보여 줍니다. 메모의 칠 아래에 깔리고, 글자는 건드리지 않습니다. 칠할 수 없는 브라우저에서는 판의 줄이 그렇다고 말합니다.
- 설명과 메모 숨기기: 설명을 끄면 여백 카드, 접힌 줄, 보조 도구 줄과 인용에 칠한 바탕이 사라지고 여백이 다시 놓입니다. 메모를 끄면 메모 카드와 칠이 사라집니다. 메모를 끈 채 새 메모를 쓰거나 목록에서 메모로 가면 메모가 다시 켜집니다. 한국어 설명은 줄이 바뀔 때 낱말을 끊지 않습니다.
- AI 도구: `save_paper_glosses`가 `summaries`(한 번에 120개, 언어마다 1,000개, 한 요약 300자)와 `key_sentences`(한 번에 60개, 언어마다 200개, 그 블록의 문장을 그대로 8~600자)를 받고, `remove.summaries`(블록 id)와 `remove.key_sentences`로 뺍니다. `get_paper_reading`은 읽은 쪽의 요약과 핵심 문장을 돌려주고, 저장 결과는 아직 요약이 없는 문단 수를 알려 줍니다. 매 차례 모델이 받는 도구 목록은 그대로이고, papers 묶음 설명이 약 560자 늘었습니다.
- 지침: 읽기 안내(`get_guide(topic:reading)`)가 좋은 요약(문단마다 한 문장, 많아야 두 문장, 문단에 없는 말을 더하지 않음)과 핵심 문장(온전한 문장을 그대로, 초록과 관련 연구에는 두지 않음)을 말합니다. 안내는 약 720자 늘었고, 읽기를 만들 때 한 번 읽습니다.
- 요청: 새 원문 읽기를 부탁하는 글이 요약과 핵심 문장까지 부탁합니다. 판의 'AI에게 맡기기'는 없는 것만 부탁합니다(요약이 없는 문단 수를 적어서).
- 문헌 페이지의 원문 읽기 줄에 요약 수가 붙습니다(뜻 36 · 설명 6 · 요약 13 · 한국어).
- 데모: arXiv 데모 논문에 한국어 요약 13개와 핵심 문장 7개가 있습니다. PDF 데모에는 없어서 판에서 'AI에게 맡기기'를 볼 수 있습니다.
- 크기(gzip, 0.90.1 대비): 읽기 화면 코드 +2.4KB, 스타일 +0.9KB, 앱 첫 화면 +0.4KB.
- 슬라이드: 글자를 힌팅하는 화면(CI의 리눅스 러너가 그렇습니다)에서도 슬라이드의 줄이 상자를 넘지 않습니다. 줄은 글꼴의 실제 폭으로 나누는데, 힌팅은 글자마다 폭을 화면 크기에서 반올림해 한국어 줄을 2~3% 넓혔습니다(R1 셋째 장의 한 줄이 상자 1,136에 1,142). 슬라이드 그림, 요소 그림, 도식, 발표 화면의 차트가 이제 글자를 실제 폭 그대로 놓습니다(`text-rendering: geometricPrecision`). 0.90.0과 0.90.1을 CI에서 멈춘 그 시험입니다.
- 시험: 빈 프로젝트 시험이 가입 직후 주소에 남은 데모 프로젝트 대신 새로 만든 프로젝트를 기다립니다(0.90.1 CI의 다른 실패). 브라우저 시험은 `E2E_FONT_HINTING=full`로 CI처럼 힌팅한 글자를 그릴 수 있습니다.
- 배포: 마이그레이션은 없습니다(요약과 핵심 문장은 언어별 풀이에 들어가고, 데이터베이스 검사는 그대로 받습니다). MCP 함수(`research-loop-mcp`)를 올린 뒤 태그로 사이트와 플러그인을 올립니다. 0.90.0과 0.90.1은 CI에서 멈춰 사이트와 플러그인으로 나가지 않았으므로, 그 두 버전의 내용도 이번에 함께 나갑니다.

## 0.90.1 — 2026-10-27

Research Loop is in order (0.90.0's work, which ships here): every place has one name, every screen is drawn from one system of space, type and colour, and each screen leads with what you came for. The research tree is a table of branches that says what each line has learned; empty places say what is missing; the latest records say who made each one. Deadlines sent to Google Calendar are labelled as each language writes a label.

- 0.90.0은 CI에서 멈춰 사이트와 플러그인으로 나가지 않았습니다. 0.90.1이 0.90.0의 내용을 그대로 싣습니다(아래 0.90.0 항목).
- 구글 캘린더로 내보내는 마감 제목은 언어마다 이름표를 쓰는 방식대로 씁니다: `마감: 제목`, `Deadline: …`, `締切: …`, 프랑스어는 쌍점 앞에 줄바꿈 없는 공백을 둔 `Échéance : …`. 캘린더 함수를 배포하면 다음 동기화에서 내보낸 마감 제목이 한 번씩 바뀝니다.
- 시험: 캘린더 Deno 시험이 새 제목을 기대하고, 슬라이드 맞춤 브라우저 시험은 슬라이드마다 그 글꼴을 다 받은 뒤 잽니다(느린 서버에서 글꼴 조각이 늦게 와도 결과가 같음).
- 배포: 마이그레이션은 없습니다. MCP 함수(`research-loop-mcp`)와 캘린더 함수 둘(`google-calendar`, `google-calendar-worker`)을 올린 뒤 태그로 사이트와 플러그인을 올립니다.

## 0.90.0 — 2026-10-27

Research Loop is in order: every place has one name, every screen is drawn from one system of space, type and colour, and each screen leads with what you came for. The research tree is a table of branches that says what each line has learned; empty places say what is missing and how to fill it; the latest records say who made each one, a person or whose AI. In the AI apps' panels, a record's title field shows its edge while edited and empty lists say what gathers there.

- 이름과 자리(1부): 갈 곳마다 이름이 하나입니다. 색인의 항목, 화면의 제목, 경로의 끝이 같은 말을 씁니다(내 연구, 프로젝트 이름, 연구 기록, 노트, 정리할 메모, 맡긴 작업, AI에게 맡기기, AI 연결). 할 일과 AI 협업은 색인이 연 범위를 따르고, 화면 안의 프로젝트 고르기는 없어졌습니다. 도구 서랍 대신 내보내기는 프로젝트 설정과 계정 화면에, 시각화 가이드는 연구 기록의 머리와 검색에 있습니다.
- 체계(2부): 공간 열 단계, 글자 여섯 크기와 세 굵기, 모든 색은 토큰, 층마다 하나의 모서리, 떠 있는 것만 그림자. 단추와 칸은 36px(작은 것 32px, 터치 44px)이고, 초점은 칸 가장자리의 2px 고리입니다. 값 사이의 가운뎃점은 쉼표와 괄호로, 링크 끝의 화살표는 낱말로, 범위는 `1~300`으로 씁니다. 작성 가이드 개정 50.
- 화면(3부): 연구 트리는 가지의 표입니다. 상태마다 묶음(살아있는 가지, 보류 중인 가지, 결론이 난 가지, 접힌 폐기된 가지), 줄마다 배운 것 한 문장과 걸음 수, 연구 날짜. 첫 화면은 노트북 한 화면에 들어옵니다. 빈 자리는 무엇이 없는지와 채우는 법을 한 문장으로 말하고, 화면마다 그 화면에 온 까닭이 맨 앞에 옵니다. 제목 속 개수는 모두 제목 옆으로 나왔습니다.
- 데이터셋 목록이 다른 기록 목록과 같은 머리, 검색, 줄을 씁니다.
- 최근 수정한 기록과 최근 추가에 만든 사람이 붙습니다. 사람의 이름, 또는 누구의 AI인지(`Claude (오정석의 AI)`). 기록되지 않았으면 붙지 않습니다.
- 패널: 기록 페이지의 제목 칸이 편집 중에 가장자리를 그리고, 빈 기록 목록이 무엇이 모이는지 말합니다.
- 배포: 가장 새 릴리스 태그만 사이트와 플러그인으로 나갑니다(옛 태그는 검사만). 마이그레이션은 없습니다. MCP 함수(`research-loop-mcp`)를 올린 뒤 태그로 사이트와 플러그인을 올립니다.

## 0.86.0 — 2026-10-26

Your AI finds what a job needs in fewer steps and less text: tools are grouped by the job and listed in a line each before any schema, writes return what they made, and a scheduling write returns the next planning token. The guides take what good public skills do well. Tables mark the best value among what competes, such as the best model on each dataset; a table with a row per method and condition is drawn with a colour per method; names in charts are read whole; and a reading's notes say what they explain.

- 도구 묶음을 하는 일로 다시 나눴습니다(열 개). 논문 읽기는 `papers`, 그림 올리기는 `media`로 나뉘었습니다. `describe_tools(group)`은 도구마다 한 줄 쓰임새만 돌려주고(묶음 하나가 130~290토큰), 스키마는 부를 도구의 이름으로 받습니다. 웹 그림 하나를 가져오는 데 읽는 양이 1,910토큰에서 461토큰으로, 논문 읽기 하나를 여는 데 3,640토큰에서 431토큰으로 줄었습니다. 매 차례 모델이 받는 목록과 접속 지침은 0.85.0보다 10토큰 늘었습니다(4,419 → 4,429).
- 쓰기 결과: 바로 만든 기록은 id로 알려 주고, 데이터베이스의 작업·이벤트 id처럼 모델이 쓰지 않는 것은 뺍니다. 영향 확인 안내는 연구 기록을 바꾼 쓰기에만 붙습니다(할 일·일정·토론에는 붙지 않음).
- 일정 쓰기(할 일, 마감, 주간 계획)는 다음 계획 토큰과 그 쓰기가 닿은 날의 부하를 돌려줍니다. 연달아 쓸 때 일정을 다시 읽지 않습니다. 시험의 '이번 주 목표와 할 일 셋'이 호출 10번에서 7번으로, 모델이 다시 읽은 글자가 37% 줄었습니다.
- 지침(쓰기 개정 49, 문헌 개정 6): AI가 쓴 티가 나는 표현(본론 전 뜸 들이기, 맺음 구호, 부풀린 의의, 겹친 얼버무림, 문서에 대한 문장 등)을 저장 전에 거르고, 고쳐 쓰기는 사실을 더하지 않습니다. 검색은 어디서 언제 찾았는지 적고 '선행 연구 없음'이라고 쓰지 않습니다. 문헌의 요약은 반박할 수 있는 핵심 주장 한 문장이고, 여러 논문은 질문·주제별로 묶습니다. 실험 반복은 주장 수준으로 합니다(학습 주장은 seed, 일반성 주장은 다른 데이터셋·과제).
- 표의 가장 좋은 값: 행이 데이터셋이고 열이 모델이면 같은 데이터셋 안에서 가장 좋은 모델을 칠합니다(전에는 모델마다 가장 점수 높은 데이터셋을 칠했습니다). 첫 열 머리글(Dataset, Task, Benchmark, 데이터셋, 지표 …)과 단위를 읽으므로 이미 쓴 표도 다시 쓰지 않고 바르게 보입니다. 그림 설정에 '가장 좋은 값: 자동 · 행마다 · 열마다'가 생겼고, AI는 가장 좋은 값을 손으로 굵게 칠하지 않고 `bestIn`으로 정합니다.
- 그림의 긴 이름: 히트맵 열 이름은 칸 위에 세 줄까지 쓰고, 넘치면 45°로, 칸이 좁으면 세워서 씁니다. 행 이름은 두 줄까지 씁니다. 막대·점·선 그림의 이름 붙은 가로축 값은 하나도 건너뛰지 않고 두 줄이나 사선으로 씁니다. `attention_entropy`처럼 띄어쓰기 없는 이름은 `_ - / .`와 camelCase 경계에서 끊습니다.
- 긴 표: '방법 × 출력 × batch'처럼 한 행이 방법 하나와 조건 하나인 표에서 한 열을 그리면, 조건마다 한 자리, 방법마다 한 색으로 그리고 범례를 붙입니다(히트맵은 방법을 세로로, 조건을 가로로). 가장 좋은 값은 같은 조건 안에서만 비교합니다. 조건이 저마다 열로 있는 표에 해당하며, 그림 한도는 행 수가 아니라 조건 수로 셉니다. 실제 분석 페이지의 24행 처리량 표가 같은 색 막대 24개에서 네 자리 × 여섯 색이 됐습니다.
- 표 칸은 단어와 숫자 중간에서 줄을 바꾸지 않습니다('93.9|9', 'ba|tc|h'였던 칸은 열이 넓어지고, 넘치면 표가 옆으로 넘어갑니다). 경로처럼 띄어쓰기 없이 40자가 넘는 칸만 아무 데서나 끊습니다.
- 한 결과가 같은 질문의 두 회차에 쓰이면 결과 페이지에 '답하는 질문'을 한 번만 씁니다.
- 결과 지침: 설정·데이터·평가 방식은 실험 페이지에 두고 링크합니다. 조건은 행 이름에 붙이지 않고 열마다 나눕니다. 숫자는 본문처럼 씁니다(1,024; −0.3). 예시는 주장을 보이는 두세 개만 고른 이유와 함께 둡니다. 확인한 것과 못 한 것, 사용자 지시, 대기열 상태 같은 작업 과정은 답에 쓰고 페이지에 쓰지 않습니다. 점마다 '~로 확대하지 않는다'를 덧붙이지 않습니다.
- 논문 읽기: 설명마다 무엇의 설명인지 첫 줄에 씁니다(인용한 말, 식 (3), Figure 2, Table 1, 이 문단). 좁은 화면에서 접힌 설명의 단추도 같습니다. 식·그림·표·문단 전체에 단 설명을 가리키면 그 블록이 함께 밝아지고, 블록을 가리키면 그 설명이 밝아집니다. 키보드로 옮겨 가도 같습니다.
- 플러그인: 읽기 순서 노트(`get_reading_guide`)와 논문 읽기(`get_paper_reading`)가 이름으로 헷갈리지 않게 설명을 고쳤고, 참고 문서가 새 묶음 이름을 씁니다.
- 배포: 마이그레이션 `20261026190000_table_chart_best_in`을 적용한 뒤 MCP 함수(`research-loop-mcp`)를 올리고, 태그로 사이트와 플러그인을 올립니다.

## 0.85.0 — 2026-10-26

Paper readings can now get their missing figures from your AI: where a copy has no picture, the AI puts in the paper's own figure, fetched from the web with its source or cut from the PDF page, and the caption says which AI put it there. A figure you put in stays yours. Readings also carry aids where the paper explains: an equation to move, with its symbols, its derivation line by line and values to try, or an explainer that steps through a method. Each is drawn only when opened, and goes into the basket like any figure.

- 원문 읽기에서 그림이 빠진 자리를 AI가 채웁니다. 새 MCP 도구 `place_reading_figure`는 논문 자신의 그림을 웹 주소로 가져오거나(서버가 공개 인터넷에서 받아 출처를 남깁니다) AI가 PDF 쪽에서 잘라 올린 그림을 넣습니다. 사본을 마쳤을 때와 arXiv 그림을 다 복사했을 때 결과가 빈 그림의 이름을 알려 줍니다.
- 캡션 아래에 누가 넣었는지가 보입니다. 'Claude가 가져온 그림'(출처 줄과 함께), 'Claude가 PDF 3쪽에서 잘라 넣은 그림'입니다. 사람이 넣은 그림은 AI가 바꾸지 못하고, 사람은 AI가 넣은 그림을 바꾸거나 뺄 수 있습니다.
- 읽기 머리의 '그림 2개가 아직 PDF에만 있습니다' 옆에 'AI에게 맡기기'가 생겼습니다. 빠진 그림의 이름을 담은 요청으로 AI 요청 창이 열립니다.
- 식 풀어 보기와 도해: AI가 뜻·설명을 달 때 논문마다 1–3개를 함께 답니다. 식 아래 '식 (2) 풀어 보기'를 펼치면 기호를 가리켜 보고, 유도를 한 줄씩 넘기고, 값을 움직여 볼 수 있습니다. 방법을 말하는 문단 아래 '도해로 보기'는 단계별 도해입니다. 페이지의 수식·도해와 같은 것이라 같은 검사(손으로 푼 점검값)를 받고, 펼칠 때 처음 그리며, 바구니에 담아 페이지와 발표에 씁니다.
- 읽다가 식이나 방법을 AI에게 물으면, 그 프로젝트를 편집할 수 있는 AI는 답과 함께 그 블록에 식 풀어 보기나 도해를 달고 답에 그렇게 적습니다.
- 데모 논문의 식 (2)에 식 풀어 보기(논문의 설정대로 24층, 하한은 층마다 고르게 나눈 몫의 4%쯤), Method 첫 문단에 다섯 단계 도해가 붙었습니다.
- 코드: 로그인한 앱의 첫 화면 코드가 0.3KB(gzip) 늘었고, 읽기 화면은 코드 1.1KB와 스타일 0.2KB가 늘었습니다. 식과 도해를 그리는 코드는 연구 페이지가 이미 받는 것을 함께 씁니다.
- 배포: 마이그레이션 `20261026180000_ai_reading_figures`를 적용한 뒤 MCP 함수(`research-loop-mcp`)를 올리고, 태그로 사이트와 플러그인을 올립니다.

## 0.84.0 — 2026-10-26

Lab templates now show what they hold: the deck's template card draws the current slide on yours with its layouts, colours and faces, turns the page number off and sets the footer, and takes a dropped file; the preview draws a cover, a section and a body slide on it. EMF and WMF logos are drawn, fixed text wraps, and saved files keep the template's placeholders and fonts. Templates exported from Google Slides now work. Paper contents give long section names room, and the home page's Sign in no longer breaks apart at mid widths.

- '발표 전체 → 연구실 양식'이 카드 하나가 됐습니다. 이 슬라이드를 그 양식으로 그린 그림, 이름, 표지·절 구분·본문이 쓰는 양식의 레이아웃, 색 견본, 제목·본문 글꼴, 쪽 번호 켜고 끄기, 바닥글 글, '다른 양식으로 바꾸기', '양식 빼기'가 있습니다. 양식이 없으면 PowerPoint 파일을 끌어다 놓거나 고르는 자리가 있고, 최근 양식 세 개는 저마다 자기 그림으로 그려집니다.
- 미리보기는 이 발표의 표지·절 구분·본문 세 장을 양식에 그리고, 장마다 어느 레이아웃인지 적습니다(없으면 '본문 레이아웃으로'). 색, 글꼴과 크기, 쪽 번호, 바닥글, 화면이 그리지 못한 것도 보입니다. 휴대폰에서는 미리보기가 옆으로 넘어갑니다.
- 쪽 번호와 바닥글은 발표마다 정하고 실행 취소 한 번으로 돌아갑니다. 화면, 썸네일, 발표 화면, PPTX가 같습니다. 표지에는 둘 다 없습니다.
- EMF·WMF 로고를 브라우저에서 PNG로 그립니다(rtf.js, 양식에 메타파일이 있을 때만 받음). PPTX에는 원본이 그대로 갑니다. 양식의 고정 글은 상자 폭에서 줄을 바꿉니다.
- PPTX: '한 문장' 슬라이드의 문장이 제목 개체 틀이 되고, 마스터에만 있는 쪽 번호·바닥글도 개체 틀로 들어가며, 양식에 묻힌 글꼴이 함께 갑니다(하나 10MB, 모두 25MB까지).
- Google Slides에서 내보낸 양식(연구실 실제 양식으로 확인)을 제대로 읽습니다. 레이아웃 종류 대신 개체 틀과 이름으로 표지·절 구분·본문을 고르고, 개체 틀에 적힌 글꼴(Noto Sans KR)을 쓰고, 글상자로 그린 쪽 번호를 쪽 번호 자리로 읽습니다. 전에는 이런 양식으로 PPTX를 저장하면 기본 모양으로 저장됐습니다.
- 표지와 절 구분의 제목·부제가 양식 자리의 크기·굵기·색·정렬·세로 위치를 따릅니다(본문 슬라이드 제목은 이미 그랬습니다). 이미 양식을 쓴 발표의 표지 제목이 가운데로 오거나 크기가 바뀔 수 있습니다.
- 랜딩: 영어·프랑스어·일본어 화면에서 창 폭에 따라(900–1,330px, 프랑스어는 휴대폰 폭에서도) 머리의 '로그인'이 한두 글자씩 세로로 쪼개지던 것을 고쳤습니다. 머리의 단추와 링크는 줄을 바꾸지 않고, 섹션 링크는 자리가 모자라면 가운데에서 비켜나다가 그래도 모자라면 숨습니다. 휴대폰에서 수식 예시의 항목 설명이 화면의 3분의 1 폭에 갇히던 것도 고쳤습니다. 320–1,600px, 네 언어에서 시험합니다.
- 앱 안에서도 같은 종류를 고쳤습니다. 할 일 머리의 '목록/일정' 전환(영어 Schedule, 프랑스어 Planning), 휴대폰 일정의 주·월 전환(이제 한 줄을 차지합니다), 기록 페이지 속성의 질문 링크(한국어가 음절 중간에서 끊김), 시각화 가이드의 이름, 기록 목록의 종류 칸(일본어 データセット)입니다. 로그인한 앱의 모든 화면을 다섯 폭, 네 언어로 시험합니다.
- 발표 편집 화면의 접힌 묶음 이름('발표 전체' 등)이 옆의 긴 양식 이름에 밀려 '발표 전 / 체'로 쪼개지지 않습니다.
- 바구니: 빼기·비우기·되돌리기가 화면 읽기 프로그램에 말해지고, 창의 이름이 한 줄로 맞춰지며, 휴대폰에서 알림이 시트를 가리지 않습니다. 같은 알림은 한 번만 뜹니다.
- 논문 읽기의 차례: 넓은 화면에서 차례 칸이 넓어지고(216–272px) 절·소절 번호가 한 열로 서서 긴 이름도 깔끔히 접힙니다. 길면 끝이 흐려지고 읽는 절이 차례 안에서 따라 보입니다.
- 첫 화면의 코드는 그대로이고 공통 스타일이 0.1KB(gzip) 늘었습니다. 로그인한 앱의 코드는 2.0KB 늘었고, 발표 편집 화면은 코드가 0.5KB 줄고 스타일이 0.4KB 늘었습니다. 양식 미리보기(1.7KB와 스타일 0.7KB), 양식 읽기(13.1KB), 양식으로 PPTX 저장(5.1KB)은 쓸 때 받고, 메타파일 그리기(rtf.js, 28KB)는 양식에 EMF·WMF 그림이 있을 때만 받습니다.
- 배포: 마이그레이션이 없습니다. MCP 함수(`research-loop-mcp`)를 올린 뒤 태그로 사이트와 플러그인을 올립니다.

## 0.83.0 — 2026-10-26

Paper readings now have a place of their own in each project, Reading (논문 읽기), next to the research flow in the project menu: the papers you are in the middle of, with where you stopped on any device and how long is left, every paper with how far you have read it, and adding a paper from arXiv, a PDF or a literature record. Drag over a passage to leave a memo: it is painted in place and set in the margin, kept to yourself or shared with the team, and can be asked of your own AI, which answers under it. The literature list and page say how far you have read and where your memos are.

- 프로젝트 메뉴의 연구 흐름 다음에 '논문 읽기'가 생겼습니다. 맨 위 '이어 읽기'에는 읽다 만 논문이 최근 순으로 카드로 있고, 카드마다 몇 %까지 읽었는지, 어느 절에서 멈췄는지, 남은 시간, 메모 수가 보입니다. 누르면 그 자리에서 이어 읽습니다. 아래 '모든 논문'은 읽는 중·안 읽음·다 읽음으로 고르고 제목·저자로 찾습니다. 원문 읽기가 없는 문헌은 접어 두고, 거기서 바로 원문 읽기를 만들게 합니다.
- '논문 추가'는 arXiv 주소나 번호, PDF, 이미 있는 문헌 가운데 하나를 고르면 문헌 기록을 만들고(있으면 그것을 쓰고) AI에게 원문 읽기를 요청하는 창까지 한 번에 갑니다. PDF는 이 기기에서 제목과 쪽 수만 읽고 올리지 않습니다.
- 읽던 자리와 읽은 비율이 서버에 남아 다른 기기에서도 이어 읽습니다. 바뀌었을 때만, 10초에 한 번 이하로 쓰고, 창을 닫거나 탭을 떠날 때 바로 씁니다.
- 읽다가 글을 끌어 고르면 '메모'가 맨 앞에 뜹니다(보기 전용 멤버에게도). 메모한 대목은 형광펜처럼 칠해지고, 넓은 화면에서는 여백에 카드로, 휴대폰에서는 문단 아래 접힌 줄로 보입니다. 기본은 나만 보기이고 편집할 수 있는 사람은 팀과 나눕니다. 위 줄의 '메모'가 이 논문의 메모 목록을 열고, 논문 읽기의 '메모' 탭에는 프로젝트의 모든 메모가 있습니다. 원문이 다시 옮겨져도 메모는 그 글로 자리를 다시 찾습니다.
- 메모의 'AI에게 묻기'는 프로젝트 대기열이 아니라 그 메모를 쓴 사람의 AI에게만 갑니다. AI는 대화를 시작할 때(`who_am_i`) 질문이 있다는 것을 듣고, `list_reading_questions`로 질문과 그 대목의 문단을 받아 `answer_reading_memo`로 답합니다. 답은 메모 아래에 AI 종류 이름으로 달립니다.
- 문헌 목록의 줄에 '읽는 중 62%', '다 읽음', '원문 읽기', 'AI 요청 대기 중'과 '메모 n'이 붙고, 머리에 '논문 읽기'가 있습니다. 문헌 페이지의 원문 읽기 입구는 읽기 시작한 뒤에는 '42% 읽음 메모 2'처럼 내 진행을 보여 줍니다.
- 논문 읽기에서 연 읽기 화면은 '논문 읽기'로 돌아가고, 머리 끝의 '문헌 기록'이 문헌 페이지를 위에 엽니다.
- 데모에서 처음부터 해 볼 수 있습니다. 진행과 메모는 이 탭에만 남고, AI의 답을 지어내지 않습니다.
- 첫 화면은 그대로입니다. 로그인한 앱의 코드는 11.0KB(gzip), 읽기 화면은 7.3KB 늘었고, 논문 읽기 화면(4.4KB)과 논문 추가 창(3.3KB)은 처음 열 때 받습니다.
- 배포: 마이그레이션 `20261026160000`을 먼저 적용합니다(`npm run -s migration:sql -- 20261026160000 | pbcopy`를 SQL Editor에 붙여 실행). 그전에는 논문 읽기가 진행과 메모를 읽지 못하고 '다시 불러오기'를 보여 줍니다. 다음 MCP 함수(`research-loop-mcp`), 그다음 태그로 사이트와 플러그인을 올립니다.

## 0.82.0 — 2026-10-26

A paper reading's missing figures can now be put in by the person reading. On a figure's place, Add figure opens a dialog: open the paper's PDF on this device (it is never uploaded), and the app turns to the figure's page with the part around it already chosen; adjust it by dragging or with the keys and put it in, cut sharp. A picture file or a screenshot works too, a figure that has a picture can be replaced, and the reading says where each figure came from. The AI tells the person when a copy it finished still lacks figures.

- 원문 읽기에서 그림이 빠진 자리마다 편집할 수 있는 사람에게 '그림 넣기'가 있습니다. 읽기 머리에는 '그림 2개가 아직 PDF에만 있습니다'와 'PDF에서 그림 넣기'가 있어 빠진 그림을 차례로 채웁니다. 캡션만 있고 그림 줄이 없던 그림도 자리가 생겼습니다.
- 넣기 창의 'PDF에서 자르기': 논문 PDF를 고르거나 끌어 놓으면 이 기기에서만 열고(올리지 않습니다) 그 그림이 있는 쪽을 엽니다. 캡션과 잉크로 그림 둘레를 찾아 두고, 끌거나 손잡이로, 화살표(Shift는 크게, Alt는 크기)로 고쳐 Enter로 넣습니다. 고른 부분만 선명하게(1pt에 4px) 잘라 이 문헌 기록에 올립니다. 빠진 그림이 더 있으면 '넣고 다음 그림'으로 PDF를 연 채 이어 갑니다. 쪽 수나 제목이 다르면 같은 논문인지 확인하라고 알립니다.
- '그림 파일': 그림을 고르거나 끌어 놓거나 ⌘V·Ctrl+V로 붙여 넣습니다(PNG·JPEG·WebP·GIF, 25MB). 그림이 있는 자리에는 '바꾸기'가 있고, 바꿀 때 지금 그림이 제목 옆에 작게 보입니다. 사람이 넣은 그림은 '넣은 그림 빼기'로 되돌립니다.
- 사람이 넣은 그림은 캡션 아래에 'PDF 3쪽에서 잘라 넣은 그림' 또는 '직접 넣은 그림'이라고 적힙니다. 읽기본 옆에 그림 번호로 따로 두므로 AI가 사본을 다시 지어도 남고, 다른 논문이 들어오면 지워집니다. 바구니에 담으면 사람이 넣은 그림이 담깁니다.
- PDF 도구(pdf.js)는 넣기 창에서 PDF를 열 때만 받습니다. 사이트 보안 정책은 그대로입니다. 첫 화면은 그대로이고, 읽기 화면은 1.7KB(gzip) 늘었습니다.
- AI가 그림 없이 PDF 사본을 마치거나 arXiv에서 복사하지 못한 그림이 남으면, 그 수를 알려 주고 사람이 읽기 화면에서 넣을 수 있다고 전하게 합니다(사람이 이미 넣은 그림은 빼고 셉니다).
- 데모에서 데모 논문의 실제 PDF로 처음부터 끝까지 해 볼 수 있습니다('데모 논문 PDF 열기'). 넣은 그림은 새로 고치면 사라집니다.
- 배포: 마이그레이션 `20261026100000`을 먼저 적용합니다(`npm run -s migration:sql -- 20261026100000 | pbcopy`를 SQL Editor에 붙여 실행). 그전에는 읽기 화면은 전처럼 열리고 그림 넣기만 실패합니다. 다음 MCP 함수(`research-loop-mcp`), 그다음 태그로 사이트와 플러그인을 올립니다.

## 0.81.1 — 2026-10-26

Exported decks are now checked the way PowerPoint reads them: every part against the Office Open XML schemas and the package's references and ids, in the test suite. The check found and fixed three faults that every PPTX carried (the notes master listed after the slides, content types for parts that were not there, repeated shape ids in masters from LibreOffice templates). A paper reading's text width can now be set from its bar, and a template's footer prompt is no longer taken for a footer.

- 내보낸 PPTX를 PowerPoint가 읽는 방식으로 검사합니다. 모든 XML을 Office Open XML 표준 스키마(ISO/IEC 29500 Transitional)로 검사하고, 관계·콘텐츠 형식·개체 id·마스터·레이아웃·슬라이드 id가 맞는지도 봅니다. 양식 없는 발표, 양식 발표, LibreOffice로 만든 양식 발표를 시험이 매번 검사합니다(CI는 Python lxml을 설치합니다).
- 검사가 찾은 세 가지를 고쳤습니다. `presentation.xml`이 노트 마스터를 슬라이드 목록 뒤에 적던 것(지금까지의 모든 PPTX), 없는 부분을 가리키는 콘텐츠 형식, LibreOffice 양식에서 옮겨 온 마스터의 겹친 도형 id입니다. PowerPoint는 예전 파일도 열었지만, 이제 표준이 허락하는 모양 하나로 씁니다.
- 원문 읽기 위 줄에 '본문 폭'이 생겼습니다. 끌면 글이 바로 넓어지거나 좁아지고(520–960px, 기본 680), 폭의 이름과 한 줄에 들어가는 글자 수를 보여 줍니다. 고른 폭은 이 기기에 모든 읽기 공통으로 남고 '기본 폭'으로 돌아갑니다. 넓은 폭이 차례·메모와 함께 들어가지 않으면 차례를 위 줄로 접고, 글이 화면을 이미 채우는 좁은 화면에서는 보이지 않습니다.
- LibreOffice가 양식의 바닥글 자리에 써 두는 'Footer'·'<footer>'·'바닥글' 같은 안내 글을 연구실의 바닥글로 쓰지 않습니다.
- 배포: 마이그레이션은 없습니다. 이 버전 번호를 알리도록 MCP 함수를 다시 올리고, 태그로 사이트와 플러그인을 올립니다. 0.72.0부터 한 번에 올린다면 0.72.0–0.79.0의 마이그레이션 여섯 개를 번호 순서대로 먼저 적용합니다.

## 0.81.0 — 2026-10-26

A deck can now take a lab's own PowerPoint template. Imported in the deck editor, the template is read in the browser and previewed on the deck's cover and current slide; used, every slide flows into its title and body places on its own ground and art, and the exported PPTX is written on the template's own master, with titles, page numbers and footers in its placeholders and words in its theme fonts.

- 발표 편집 화면 '발표 전체'의 모양 목록 끝에 '연구실 양식'이 생겼습니다. 'PowerPoint 양식 가져오기'로 연구실의 .pptx나 .potx를 고르면 브라우저 안에서 읽고(서버에 보내지 않습니다), 이 발표의 표지와 지금 슬라이드를 그 양식에 그려 보여 줍니다. 찾은 레이아웃·그림·제목 서체와, 화면이 그리지 못하는 그림·효과·도형의 수도 말합니다.
- '이 양식 쓰기'를 누르면 모든 슬라이드가 양식의 제목 자리와 본문 자리로 흐릅니다. 제목은 그 자리의 크기·색·정렬·세로 맞춤을 따르고, 열두 열은 본문 자리 너비로 나뉩니다. 표지·절 구분은 양식의 표지·구역 머리글 레이아웃에, 쪽 번호와 바닥글은 양식의 자리에 놓입니다. 실행 취소 한 번으로 돌아오고, '양식 빼기'로 바탕 모양으로 돌아갑니다.
- 색과 서체도 양식에서 나옵니다. 배경·글·제목 색과 테마의 강조색(배경 위에서 읽히는 것만), 제목 크기와 굵기, 명조·고딕을 양식에서 읽고, 표와 차트, 목록 표시는 가장 가까운 모양(선명·논문·무대)을 따릅니다.
- PPTX로 내보내면 양식의 첫 마스터가 그대로 들어갑니다. 슬라이드마다 그 종류의 레이아웃을 쓰고, 제목·부제·절 요약은 개체 틀, 쪽 번호는 슬라이드 번호 필드, 글은 테마 서체로 씁니다. 10인치 16:9 양식(Google Slides)은 와이드에 맞게 늘립니다. 4:3 양식은 받지 않고 PowerPoint에서 바꾸는 길을 알려 줍니다. 양식 파일을 읽지 못하면 기본 모양으로 저장했다고 말합니다.
- 양식은 발표 페이지의 블록(요약, 원본 .pptx, 그림)으로 저장되고 저장할 때 한 번 올립니다. 최근에 저장한 양식 셋은 이 기기에 사람마다 남아 다음 발표에서 바로 고를 수 있고(로그아웃하면 지웁니다), 같은 프로젝트의 다른 발표에 쓴 양식도 고를 수 있습니다. 양식 블록이 망가진 발표는 양식 없이 열리고 그렇다고 알립니다.
- 매크로가 든 파일, DOCTYPE, 25MB를 넘는 파일은 받지 않고, 양식의 XML이나 SVG를 그대로 쓰지 않습니다. 화면의 양식 그림은 읽은 숫자·색·이스케이프한 글로만 짓고, 그림은 페이지가 가진 주소로만 그립니다.
- 배포: 마이그레이션이 없습니다. MCP 함수를 다시 올리면 발표 참고 도구의 안내(양식 블록을 그대로 두라)가 나가고, 그다음 태그로 사이트를 올립니다.

## 0.80.0 — 2026-10-25

Things worth a slide can now be gathered while reading. On a page or in a paper reading, Add on a figure, plot, table, equation or diagram, or Add to basket on selected words, keeps a copy in the project's basket on this device. The deck editor shows the basket beside the slides: press an item to put it in the chosen slot or the first free slot that takes it, else on a new slide right after, or drag it onto a slot. Each item keeps where it came from, and a paper's figure its credit.

- 읽다가 슬라이드에 쓸 것을 바구니에 담습니다. 페이지와 원문 읽기의 그림·Python 그림·표·수식·도해마다 '담기'가 있습니다. 마우스를 올리거나 키보드 초점이 오면 오른쪽 위에 보이고, 손가락 화면에서는 그것 아래에 있어 아무것도 가리지 않으며, 표로 그린 차트에서는 그림/표 전환 바로 앞에 있습니다. 글을 고르면 도구 줄에 '바구니에 담기'가 생깁니다. 담은 것은 담은 때의 모습 그대로 남습니다.
- 바구니는 사람과 프로젝트마다 이 기기에 둡니다(서버를 부르지 않습니다). 새로 고침과 다른 창에서도 같고, 로그아웃하면 이 기기에서 지워집니다. 50개, 항목 하나 200KB, 바구니 하나 1MB까지 담고, 같은 것은 한 번만 담깁니다. 프로젝트를 고칠 수 있는 사람에게만 보이고, ChatGPT·Claude 안의 패널에는 없습니다.
- 페이지 창과 원문 읽기의 위 줄에 '바구니 3'이 생깁니다. 열면 무엇을 어디서 담았는지 보이고, '원래 자리'로 그 블록에 가거나, 하나씩 빼거나, 비울 수 있습니다(창이 열려 있는 동안 '되돌리기'). '발표로 가기'가 이 프로젝트의 발표 화면을 엽니다. 휴대폰에서는 아래에서 올라오는 판입니다.
- 발표 편집 화면 오른쪽의 '바구니'에서 슬라이드로 넣습니다. 누르면 고른 빈 칸에, 없으면 이 슬라이드에서 그것을 받는 첫 빈 칸에(글은 문단이 들어갈 칸에만), 없으면 바로 다음에 그것에 맞는 레이아웃의 새 슬라이드로 들어갑니다(제목은 캡션의 첫 문장). 끌면 받는 칸이 점선으로 보이고, 빈 칸에 놓으면 넣고, 채워진 칸에 놓으면 바꾸고, 왼쪽 목록의 슬라이드에 놓으면 그 슬라이드로 갑니다. 한 번 넣기는 실행 취소 한 번이고, 넣은 것도 바구니에 남습니다.
- 넣은 것은 출처를 잃지 않습니다. 슬라이드의 출처 줄에 담은 페이지나 논문이 더해지고, 논문의 그림은 '그림: 저자 · 라이선스 · arxiv.org'를 달고 가서 0.76.0의 라이선스 점검을 그대로 받습니다. 고른 글 속 수식은 TeX로 옮깁니다.
- 발표 목록은 바구니에 무엇이 있으면 위에 한 줄로 알립니다.
- 첫 화면에는 위 줄의 수와 '담기' 단추만 들고, 바구니 창과 보관소, 담는 일은 처음 쓸 때 불러옵니다.
- 배포: 마이그레이션이 없습니다. MCP 함수를 다시 올리면 이 버전으로 다시 지은 ChatGPT·Claude 패널이 나갑니다(패널에는 바구니가 없고 페이지는 전처럼 보입니다). 그다음 태그가 사이트와 플러그인을 올립니다.

## 0.79.0 — 2026-10-25

A paper that is not on arXiv can now be read from its PDF. The AI reads the PDF with its own tools and transcribes it a few pages at a time with save_paper_text; Research Loop keeps the transcription, builds the same kind of reading from it with citations, figures, tables, equations and sections linked, and tells the AI what looks wrong so it can send a page again. The reader says the text is an AI's copy, gives each part's PDF page and asks readers to check the PDF before citing.

- arXiv에 없는 논문도 원문 읽기를 만들 수 있습니다. AI가 PDF를 자기 도구로 읽어 몇 쪽씩 마크다운으로 옮기면, 서버가 그 원고로 같은 읽기본을 짓습니다. arXiv에 있는 논문은 지금처럼 arXiv의 HTML에서 가져옵니다(정확하고 공짜입니다).
- 서버는 옮긴 원고를 쪽마다 보관하고 부를 때마다 처음부터 다시 짓습니다. 쪽 넘김에 끊긴 문단과 목록을 잇고, 번호로 제목 수준을 정하고, 초록과 참고문헌을 따로 두고, 캡션을 그림·표·알고리즘과 짝짓습니다. 번호 인용은 모든 번호가 참고문헌에 있을 때, 저자–연도 인용은 성과 연도가 한 항목에만 맞을 때 참고문헌을 열고, 'Figure 2', 'Table 1', 'Eq. (3)', 'Section 4'는 그 자리로 갑니다.
- 의심되는 곳은 거절하지 않고 점검으로 AI에게 알립니다. 다른 쪽보다 훨씬 짧은 쪽, 빈 쪽, 짝 없는 $, 닫히지 않은 수식·코드·주석, 칸 수가 다른 표 줄, 표 없는 표 캡션, 참고문헌에 없는 인용, 짝 없는 각주, 건너뛴 절 번호, 언급했지만 없는 그림과 표입니다. AI는 그 쪽을 다시 보내 고칩니다.
- MCP 도구 `save_paper_text`(편집자 이상)가 생겼습니다. 한 번에 40,000자, PDF 500쪽까지, 1쪽부터 빠짐없이 보내고, 보낸 쪽을 다시 보내면 그 쪽이 바뀝니다(뜻과 설명은 그 단어가 남아 있으면 그대로). 결과가 쓴 블록의 id와 첫 단어를 알려 주므로 AI는 원문을 다시 읽지 않고 뜻과 설명을 답니다. 그림은 AI가 잘라 올릴 수 있을 때만 이 기록에 올리고, 아니면 'PDF n쪽' 자리로 둡니다. PDF를 옮기는 지침 `get_guide(topic:reading, section:pdf)`(2,295자)는 PDF일 때만 읽습니다.
- 읽기 화면은 사본임을 숨기지 않습니다. 메타 줄에 'Claude가 PDF에서 옮긴 사본'(학회와 DOI도), 차례에 PDF 쪽 번호, 그림 자리에 'PDF n쪽'(공개된 PDF면 그 쪽으로 가는 링크), 끝에 '인용하기 전에 PDF와 대조하세요'가 있습니다. 옮기는 중인 사본도 열리고, 어디까지 옮겼는지 말합니다.
- 문헌 페이지는 모든 논문에 '원문 읽기 만들기'를 보여 줍니다(요청 글이 PDF가 필요하면 말해 달라고 합니다). 옮기는 중인 사본에는 '옮기는 중 3/12쪽'과, 편집할 수 있는 사람에게 '이어서 만들기'가 나옵니다.
- 데모의 KV 프로젝트에 PDF에서 옮긴 두 번째 설명용 가상 논문(3쪽, 600단어, 올린 그림 하나와 'PDF 3쪽' 자리 하나, 한국어 뜻 17개와 설명 3개)이 있습니다.
- 배포: 마이그레이션 `20261025230000`을 먼저 적용하고(`npm run -s migration:sql -- 20261025230000 | pbcopy`를 SQL Editor에 붙여 실행, 0.78.0의 `20261025200000` 다음), 다음 MCP 함수, 그다음 태그로 사이트와 플러그인을 올립니다. 마이그레이션 전에는 `save_paper_text`만 실패합니다.

## 0.78.0 — 2026-10-25

A literature record can now carry its paper as a reading: the paper in its own words, read like a long article, with meanings on the words a reader may not know and short explanations of hard passages, in the reader's language. An AI makes it from arXiv's HTML, built from the authors' source rather than the PDF, and writes only the meanings and explanations. The demo includes a synthetic paper to try it.

- 문헌 기록에 논문의 '원문 읽기'가 생깁니다. 논문은 원어 그대로 두고, 모를 만한 단어에만 이 논문의 문맥에 맞는 뜻을, 어려운 대목에 짧은 설명을 답니다. 뜻이 달린 단어(점선 밑줄)를 누르면 작은 창에 뜻과 풀이가, 설명은 넓은 화면에서 본문 옆 여백에, 좁은 화면에서는 문단 아래 접힌 줄로 나옵니다. 문장 전체는 번역하지 않습니다.
- 원문은 PDF를 글자로 읽은 것이 아닙니다. 서버가 arXiv가 저자의 LaTeX 소스로 만든 HTML(없으면 ar5iv)을 옮기고, 수식은 TeX로, 그림·표·인용·각주는 원래 구조대로 둡니다. arXiv의 변환이 실패한 곳이 있으면 그 수를 세어 읽기 화면에 PDF 링크와 함께 알립니다.
- 문헌 페이지의 '원문 보기' 옆에 '원문 읽기'(뜻·설명 수와 언어)가, 읽기본이 없는 arXiv 논문에는 '원문 읽기 만들기'가 나옵니다. 만들기는 이 기록과 요청 글(화면 언어로 뜻과 설명을 달아 달라는)을 채운 'AI에게 맡기기'를 엽니다. 채팅에서 AI에게 직접 부탁해도 됩니다. AI는 뜻이 필요한지, 어느 언어인지 한 번 묻고, 말하지 않으면 계정 언어로 답니다.
- 읽기 화면: 680px 단에 논문 글자(Newsreader), 900px부터 여백 설명, 1,200px부터 왼쪽 차례, 위에 돌아가기·차례·뜻 표시·뜻 언어·원문·전체 화면이 있는 얇은 줄과 읽은 만큼 차는 선. 인용을 누르면 참고문헌이, 각주 표시는 그 각주를 찾아 줍니다. 수식은 보이는 곳부터 조판하고, 긴 논문도 화면 근처부터 그려 40쪽짜리가 약 0.4초에 처음 보입니다. 다시 열면 멈춘 곳부터 이어 읽을 수 있고, 주소(`reading=1`)로 뒤로 가기·새로 고침·링크가 됩니다. 글을 고르면 지금의 '토론'·'AI에게 요청'이 그대로 떠서 뜻이 없는 단어도 물을 수 있습니다.
- MCP 도구 `import_paper_reading`(arXiv에서 원문과 그림을 가져와 만들거나 새 판으로, 뜻은 남김), `get_paper_reading`(약 24,000자씩 쪽으로), `save_paper_glosses`(뜻과 설명을 원문에 맞춰 검사해 합침, 동시 저장은 한 번 더 합치고 `expected_revision`이면 충돌을 알림)와 지침 `get_guide(topic:reading)`(1,582자)이 생겼습니다. 읽기본은 프로젝트 멤버만 보고, 쓰기는 MCP 서버의 전용 함수로만 합니다.
- 데모의 KV 프로젝트에 설명용 가상 논문(1,444단어, Python으로 그린 그림, 한국어 뜻 36개와 설명 6개)이 문헌 기록으로 들어 있습니다.
- 배포: 마이그레이션 `20261025200000`을 먼저 적용하고(`npm run -s migration:sql -- 20261025200000 | pbcopy`를 SQL Editor에 붙여 실행), 다음 MCP 함수, 그다음 태그로 사이트와 플러그인을 올립니다. 마이그레이션 전에는 읽기 도구가 실패하고 문헌 페이지에 원문 읽기가 나오지 않습니다.

## 0.77.0 — 2026-10-25

Every way of making a deck now starts in layouts and a look: a page, the research story and an AI's deck. An AI request names the deck's purpose, look and accent, and its result is slides in layouts that the review shows as slides. Graphs an AI draws from data are Python figures in the deck's look, sized to their slot, with a record of the data and code that drew them under the plot's caption.

- 페이지의 '발표 편집'이 레이아웃 발표로 열립니다. 논문은 저널 클럽(논문 모양), 나머지는 랩 미팅 진행 보고(선명 모양)로 시작하고, 상태 줄이 무엇으로 만들었는지와 '발표 전체'에서 바꿀 수 있다는 것을 알려 줍니다. 제목마다 절이 되고, 그림마다 한 장(도해는 큰 도해, 수식은 수식, 표는 표, 차트·그림은 주장+그림)에 그 그림을 읽는 글이 붙습니다. 슬라이드에 넣지 못한 글과 코드는 발표자 노트로 가고 그 수를 알려 줍니다. 레이아웃 발표에 페이지를 넣으면 절 슬라이드와 함께 그 발표의 모양으로 들어갑니다.
- 연구 이야기 초안도 선명 모양의 레이아웃 발표입니다. 표지(프로젝트·질문·발표자), 지금까지의 답, 출발점, 전환점마다 주장과 그 페이지의 그림, 접은 갈래, 지금, 남은 질문 순서입니다.
- AI 발표 요청 창에서 용도, 모양, 강조색을 고릅니다. AI는 좌표·색·글꼴 없이 레이아웃과 칸만 고른 결과(형식 2)를 보내고, 앱은 읽지 못하는 결과에 무엇이 어디서 틀렸는지 말합니다. 이미 대기 중인 이전 형식의 요청은 그대로 검토합니다.
- 검토 창은 AI의 발표를 슬라이드 그림으로 보여 줍니다. 슬라이드마다 그 슬라이드의 점검(넘침, 빈 칸, 다른 모양에 맞춘 그림 등)이 붙고, 글·노트·출처는 접혀 있습니다. AI가 올린 그림은 도착하는 대로 칸에 들어갑니다. 반영하면 레이아웃 발표 그대로 편집 화면이 열립니다.
- 플러그인의 그래프 도우미에 `slide_context`가 생겼습니다. 발표의 모양(바탕·글자·축·강조색), 칸의 크기(96px = 1인치라 그림 속 글자 크기가 슬라이드 글자 크기와 같음), 용도의 글자 크기, 발표의 글꼴(Research Loop Sans·Serif를 플러그인에 넣음)로 Matplotlib 그림을 그립니다.
- 플롯 블록이 만든 방법(`made`: 데이터·코드의 저장소 경로와 SHA-256, 커밋, 도구, 모양, 칸, 날짜)을 가질 수 있습니다. 도우미의 `figure_record`가 만들고, 페이지와 리더는 캡션 아래에 '만든 방법' 한 줄로 보여 줍니다. 발표의 모양과 다르면 다시 그리라고 알리고, 그림 파일을 바꾸면 지워집니다. 절대 경로나 저장소 밖 경로는 받지 않습니다.
- AI 지침(개정 48)의 발표 절을 레이아웃 발표와 Python 그림에 맞춰 다시 썼습니다. 요청 계약과 합쳐 4,212자로, 이전(6,931자)보다 39% 짧습니다.
- 배포: 마이그레이션 `20261025180000`을 먼저 적용하고(`npm run -s migration:sql -- 20261025180000 | pbcopy`를 SQL Editor에 붙여 실행), 다음 MCP 함수, 그다음 태그로 사이트와 플러그인을 올립니다. 마이그레이션 전에는 데이터베이스가 `made`가 든 플롯 블록을 거절합니다.

## 0.76.0 — 2026-10-25

An AI can now bring a picture from the web with import_research_image: given the image's address and the page it is on, Research Loop copies it from the public internet only and records the page, author, licence and the day it was copied. Pages, slides and PowerPoint show that source under the picture, and a licence nobody knows, or one that limits reuse, is flagged on save and before a talk. The demo's v2 page shows the StreamingLLM figure with its credit.

- AI가 인터넷의 그림을 가져올 수 있습니다. `import_research_image`에 그림 파일 주소와 그 그림이 실린 페이지 주소를 주면, 서버가 공개 인터넷에서만 가져와 프로젝트에 복사하고 출처(페이지, 작성자, 라이선스, 가져온 날)를 그림 블록에 남깁니다. 페이지는 바뀌지 않습니다. 사설·로컬 주소, 다른 포트, 10 MiB 넘는 파일, SVG, 3,200만 화소 넘는 그림은 받지 않습니다.
- 라이선스는 위키미디어의 파일 정보, arXiv 논문의 권리 링크, 페이지가 스스로 밝힌 라이선스 링크에서 읽습니다. 읽지 못하면 AI가 페이지에서 읽은 값을, 그것도 없으면 '모름'으로 둡니다.
- 페이지와 플러그인 리더는 캡션 아래에 출처 한 줄을 둡니다. 서버가 확인하지 못한 라이선스는 '(확인 안 됨)', 재사용이 제한된 라이선스는 '재사용 제한', 없으면 '라이선스 모름'으로 표시합니다.
- 슬라이드(편집 화면, 썸네일, 발표 화면, 발표자 화면)와 PPTX는 그림 캡션의 마지막 줄에 '그림: 작성자 · 라이선스 · 사이트'를 넣습니다.
- 편집기의 그림 창에서 출처 페이지, 작성자, 라이선스를 고칠 수 있습니다. 그림을 바꾸면 예전 출처는 지워집니다.
- 라이선스를 모르거나 재사용이 제한된 그림이 있는 페이지를 저장하면 쓰기는 되고 조언(`advice.image_licence`)이 붙습니다. 발표 점검도 그런 그림을 알려 줍니다.
- AI 지침(개정 47)은 원래 그림이 꼭 필요할 때(논문의 그림, 실제 장치·사진)만 가져오고, CC·퍼블릭 도메인을 먼저 찾고, 출처를 지우지 않고, 남의 그림을 우리 결과의 근거로 쓰지 말라고 합니다.
- 데모의 v2 페이지(attention sink 보존)에 StreamingLLM 논문의 그림 1을 출처와 함께 넣었습니다. 페이지의 그림 캡션은 그림과 8px 떨어지고 한국어 어절을 끊지 않습니다.
- 배포: 마이그레이션 `20261025130000`을 먼저 적용하고(`npm run -s migration:sql -- 20261025130000 | pbcopy`를 SQL Editor에 붙여 실행), 다음 MCP 함수, 그다음 태그로 사이트와 플러그인을 올립니다. 마이그레이션 전에는 데이터베이스가 출처가 든 그림 블록을 거절합니다.

## 0.75.0 — 2026-10-25

Explainers now draw each part as what it is: models as filled blocks, vectors as strips of cells, operations where arrows join as small circles with their sign, stores as cylinders, and the step to the next stage as a double arrow. Columns fit what they hold, link labels stay off other links' lines, and a slide lays a diagram out across when upright it would be too tall. The database and AI guidance accept the new kinds; a page with parts lacking a kind still saves, with a note. Exported PPTX keeps control-link dashes and link labels.

- 도해의 부품은 무엇인지에 따라 모양이 다릅니다. 모델은 채운 블록, 벡터는 칸 띠(이름은 띠 아래, 연결은 띠의 가운데로), 연산은 알약, 화살표가 만나는 곳의 원소별 연산은 기호(더하기·빼기·곱하기·나누기·이어붙이기·내적)를 그린 작은 원, 저장소는 원통, 데이터는 겹친 장, 판단은 마름모입니다. 원은 글자 없이 기호만 그리고, 이름과 설명은 올려 두거나 포커스하면 나옵니다. 종류가 없는 부품은 예전 그대로의 상자입니다.
- 다음 단계나 다음 시점으로 넘어가는 연결은 끝이 열린 두 줄 화살표로 그립니다.
- 열 너비는 담긴 것에 맞습니다. 이름의 긴 단어는 자리가 있으면 끊지 않고, 원만 있는 열은 좁게(40), 상자는 260보다 넓지 않습니다. 0.74.0에서 가로로 서던 도해는 지금도 가로로 섭니다.
- 다른 행에서 오는 갈래는 원의 위나 아래로 한 번 꺾여 들어갑니다(휴대폰의 세로 그림에서는 옆으로). 연결 이름은 다른 연결의 선 위에 놓이지 않고, 돌아가는 선은 이미 그린 선을 덜 가로지르는 쪽을 고르며, 휴대폰에서 첫 열을 건너뛰는 선은 그림 옆의 좁은 길로 돕니다. 메모로 들어가는 화살표는 글자 앞에서 멈춥니다.
- 발표의 도해(편집 화면, 썸네일, PPTX)는 상자에 맞는 가장 큰 크기를 고릅니다. 세로로 서면 너무 길어지던 도해가 가로로 섭니다.
- PPTX에서 제어 연결의 점선이 빠지던 문제(0.47.0부터)와 연결 이름이 PowerPoint·LibreOffice에서 보이지 않던 문제를 고쳤습니다. 두 줄 화살표도 그대로 나갑니다.
- AI 지침(개정 46)은 부품마다 종류를 주라고 하고, 종류마다 무엇에 쓰는지와 모양을 말합니다. 종류 없는 부품이 있는 도해를 저장하면 쓰기는 되고 조언이 붙습니다.
- 데모의 방법 페이지(M1)에서 긴 문맥 토큰은 벡터, 레이어별 예산표는 데이터로 그립니다.
- 배포: 마이그레이션 `20261025100000`을 먼저 적용하고(`npm run -s migration:sql -- 20261025100000 | pbcopy`를 SQL Editor에 붙여 실행), 다음 MCP 함수, 그다음 태그로 사이트와 플러그인을 올립니다. 마이그레이션 전에는 데이터베이스가 vector, symbol, next를 거절합니다.

## 0.74.0 — 2026-10-25

New presentations start from a purpose and a look: four purposes (conference talk, lab meeting, written report to an advisor, journal club) and four looks, with twelve layouts whose slots set sizes, alignment and a single emphasis for you. A layout change moves what has no slot to the next slide, a dragged box places its slide by hand until you restore the layout, and arrows follow the figure they point at. Older decks open unchanged and can take a look. PPTX export follows the same layout and now keeps chart values exact.

- '빈 발표'는 용도 넷과 모양 넷을 고르는 창에서 시작합니다. 용도마다 시작하는 슬라이드와 본문 크기가 다르고(학회·세미나 발표 7장 28→24pt, 랩 미팅 진행 보고 8장 24→20pt, 교수님 서면 보고 10장 20→16pt, 논문 소개·저널 클럽 11장 26→22pt), 모양(선명, 논문, 무대, 보고서)마다 서체, 색, 머리와 바닥이 다릅니다. 표지에는 발표 제목과 계정 이름, 오늘 날짜가 들어갑니다. 화살표 키로 고르고 Enter로 만듭니다.
- 레이아웃은 12개입니다(표지, 절 구분, 한 문장, 주장+그림, 큰 그림, 비교, 큰 수치, 목록, 표, 수식, 도해, 정리). 빈 칸을 누르면 그 칸이 받는 것(그림 파일, 페이지 그림, 표, 도해, 수식, 글)이 나오고, 넣기만 하면 크기와 윗선, 간격이 맞습니다. 강조색은 Focus 칸에만 쓰입니다.
- 레이아웃 단추는 이 슬라이드를 12가지로 미리 보여 주고, 칸이 모자라 옮겨질 상자 수('+1')를 고르기 전에 알려 줍니다. 남는 상자는 바로 다음 새 슬라이드로 갑니다. 실행 취소 한 번이면 돌아옵니다.
- 칸에 든 상자를 끌거나 크기를 바꾸면 그 슬라이드는 직접 배치가 되고, '레이아웃으로 되돌리기'로 돌아갑니다. 화살표(8방향)와 도형은 그림 위의 자리를 기억해서, 모양이나 제목이 바뀌어 그림이 움직이면 따라갑니다.
- '발표 전체'에서 용도, 모양, 강조색을 바꾸면 모든 슬라이드가 다시 배치되고, 이것도 실행 취소 한 번으로 돌아옵니다. 예전 발표는 그대로 열리고 그대로 저장됩니다. '모양 고르기'로 모양을 입힐 수 있습니다.
- 한국어 줄바꿈: '그 결과', '할 것'처럼 붙어 있어야 읽히는 말은 함께 넘기고, 문단의 마지막 줄에 한 어절만 남기지 않습니다. PPTX에도 같은 자리에 줄바꿈 없는 공백을 넣습니다. 예전 발표에도 적용됩니다.
- 차트의 눈금은 둥근 수(1·2·5 단위)이고, 강조할 항목 하나를 고를 수 있습니다. PPTX 차트가 값을 정수로 반올림해 보이던 문제(79.5가 80으로)를 고쳤습니다. 예전 발표에도 적용됩니다.
- PPTX는 화면과 같은 배치로 나갑니다. 보고서의 띠, 논문의 머리 선, 화면과 기준선이 맞는 글, 강조 막대, 칸에 붙은 화살표, 도해 옆 단계 목록까지 같습니다.
- 배포: 마이그레이션은 없습니다. MCP 함수를 올리고(패널이 새 형식의 발표를 읽습니다), 태그로 사이트와 플러그인을 올립니다. 배포 전에 열어 둔 탭은 새로고침해야 새 발표를 엽니다.

## 0.73.0 — 2026-10-24

Research Loop's AI guidance now says each rule once and costs less on every turn: the connect instructions and tool list a model rereads each turn are 27% smaller (28% fewer tokens), and a writing task reads 21–24% less. Who applies a write and how a made-up key is written are one line each in the connect instructions; record guides give their sections without the empty page skeleton; describe_tools says each sentence once per answer. Strict input checks are unchanged. Also fixes six details from the 0.72.0 review.

- AI가 매 차례 다시 읽는 접속 지침과 도구 목록이 27% 줄었습니다(o200k 토큰 28%). 도구 설명은 언제 부르는지, 먼저 읽을 것, 그 도구만의 규칙만 말하고, 역할별 권한 목록은 서버가 지킵니다. 엄격한 입력 검사는 그대로라 지금 받는 호출은 그대로 받고 거절하는 호출은 그대로 거절합니다.
- 누가 쓰기를 바로 적용하는지(바로 적용할 수 없는 쓰기는 검토 요청이 되고, 다른 쓰기로 다시 시도하지 않습니다)와 AI가 지어내는 키(`idempotency_key`, `request_key`)의 형식은 접속 지침에 한 줄씩만 있습니다.
- 쓰는 일 하나에 읽는 core, 기록 지침, 지침 절이 21~24% 줄었습니다. core는 입구와 검토 항목을 되풀이하지 않고 그림 규칙은 한 줄입니다. 기록 지침은 빈 페이지 뼈대 대신 절 목록(표나 코드로 시작하는 절은 그 열이나 언어)과 쓰기 한 줄을 주고, 실험 역할은 속성에만 있습니다. 유형 없이 부르면 유형 목차를 줍니다. 문헌 지침은 절마다 한 번, 영어로 줍니다(지침 개정 5). 앱이 새 페이지에 주는 뼈대와 예전 템플릿 도구의 응답은 그대로입니다.
- `describe_tools`는 한 응답에서 문장을 한 번만 말합니다. 힌트는 읽기만 하는지와 파괴적인지만 주고, 앞 도구가 이미 설명한 필드는 그 도구를 가리킵니다. 숨은 도구 설명 가운데 가장 긴 다섯이 짧아졌습니다.
- 플러그인의 research-loop 스킬이 10,240바이트에서 8,079바이트가 되었습니다. 접속 지침과 같은 뜻의 규칙(요청이 명세, 소유자 대리, 입구 하나, 작은 수정, 짧은 끝맺음)은 남겼습니다.
- 지침 시험이 과제마다 모델에게 보낸 맥락 글자를 셉니다. 기준 답안 11개는 모두 완료, 쓰기 거절 0, 맥락 합계는 23% 줄었습니다.
- 0.72.0 검토가 남긴 여섯 가지를 고쳤습니다. 구현 확인은 실험·분석 페이지가 보여 주지 않을 실행을 모두 알려 줍니다(질문이나 노트에 대한 보고도). 실행 줄의 긴 호스트·장치 목록은 넓은 화면에서도 줄 안에서 줄바꿈합니다. 페이지의 실행 줄은 '실행 정보'라는 이름으로 읽힙니다. 복사 버튼은 두 번 연달아 눌러도 제 이름으로 돌아오고, 경로를 '코드'라고 부르지 않습니다. 폴더와 출력은 C1 제어 문자와 줄·문단 구분자를 거절합니다. 엇나간 주석을 제자리로 옮겼습니다.
- 배포: 마이그레이션은 없습니다. MCP 함수(지침과 도구 목록)를 올리고 태그로 사이트와 플러그인을 올립니다.

## 0.72.0 — 2026-10-24

Analyses now read experiment, observation, cause, conclusion, and always conclude: writing guide 44 adds a results section drawn from how leading researchers report, and new analysis and experiment pages follow it. Run details leave the reading. An implementation report carries the runs an AI started (where, how, how each ended), a sentence can be carried by runs, and Implementation check gets a Runs section that experiment and analysis pages open in one click. The server flags paths, job numbers and commit hashes in result pages.

- 결과 분석은 실험 → 현상 → 원인 규명 → 결론 순서로 쓰고, 끝은 늘 결론입니다. 쓰기 지침 44에 '결과' 절이 생겼습니다. 현상에서는 결정적인 비교를 먼저 차트로 보이고, 원인 규명에서는 그럴듯한 설명을 모두 놓고 ablation, 한 변수 비교, 용량-반응, 오류 분석 같은 확인으로 가립니다. 결론은 질문에 답하는 한 문장에 확신도와 그 이유, 결론을 뒤집을 결과를 붙입니다. 근거가 약해도 "아직 아니다, 이 확인이 가려 준다"까지 씁니다.
- 새 분석 페이지는 실험 · 현상 · 원인 규명 · 결론 절로 만들어집니다. 새 실험 페이지는 질문 → 조건 → 결정적인 비교 → 모든 실행 → 실패 → 관찰 → 세부 설정 순서입니다. 예전 템플릿으로 만든 페이지는 그대로 읽히고, 손대지 않은 빈 절은 지금처럼 숨습니다. 페이지의 '재현 정보' 절은 접혀 있습니다.
- 경로, 노드, GPU, 작업 번호, 명령 같은 실행 세부는 결과 본문에서 빠지고 구현 확인의 '실행'에 모입니다. AI가 돌린 실행마다 무엇을 돌렸는지, 어떻게 끝났는지(완료·실패·중단·진행 중), 어디서 어떻게 돌렸는지가 있고, 명령과 폴더는 복사할 수 있습니다. "seed 3개씩"을 시켰는데 2개만 돌았으면 그 문장이 '일부만'으로 뜹니다.
- 실험 페이지의 핵심 결론 아래 '실행 정보 · 5건 (실패 1)'을 누르면 그 보고의 '실행'으로 갑니다. 분석 페이지에는 근거가 된 실험마다 이 줄이 있습니다.
- AI가 실험·분석 본문에 절대 경로, 작업 번호, 커밋 해시를 쓰면 서버가 옮길 곳을 알려 줍니다. AI가 핵심 결론을 '판단 보류'로 둘 때는 그걸 가려 줄 확인 하나도 적어야 저장됩니다.
- 배포: 마이그레이션 `20261024100000_implementation_runs.sql` 하나를 SQL Editor로 적용하고, 태그의 깨끗한 사본에서 MCP 함수를 올린 뒤 브랜치와 태그를 올립니다. 순서가 바뀌어 사이트가 먼저 나가도 오류는 없고, 실행 정보 줄만 보이지 않습니다.

## 0.71.1 — 2026-10-24

Rebuilds the embedded AI panels using the exact locked dependencies so their checked-in output matches a fresh CI installation. The scheduled legal revisions, independent Google AI approvals, and Free/Paid project limits from 0.71.0 are unchanged.

- 로컬에 설치된 번들러가 잠금 파일보다 새 버전이어서 CI의 패널 원본 대조가 실패하던 문제를 해결했습니다. 잠금 파일대로 다시 설치하고 정식 릴리스 명령으로 패널을 생성합니다.
- 0.71.0의 법률 문서·별도 동의·프로젝트 한도 동작과 시행 일정은 그대로 유지합니다.
- 공급자에게 확인해야 하는 전체 처리국 문의 원고를 미발송 상태로 남겼습니다.

## 0.71.0 — 2026-10-24

Google busy times reach a connected AI only after a separate, recorded approval, including for existing users. New account entitlements prepare limits of two active owned projects for Free and ten for operator-invited Paid accounts, with archived projects excluded and enforcement deferred until the announced date. Korean and English legal revisions, a change notice, preserved previous texts, and current Google data guidance explain the actual service and verified operations.

- Google 바쁜 시간 가져오기와 본인 AI 전달을 분리하고 기존 이용자도 다시 선택하도록 합니다. 본인·팀 AI 전달은 고지 버전과 승인 시각을 기록하며, 재연결·중단 때 초기화합니다.
- Free 소유 프로젝트 2개, 운영자 직접 초대 혜택 Paid 계정 10개 한도를 DB에서 적용합니다. 보관함과 다른 사람 소유 프로젝트 참여는 제외하며 기존 프로젝트는 삭제하거나 강제 보관하지 않습니다. 실제 결제는 도입하지 않습니다.
- 한영 개인정보 처리방침·이용약관 개정안과 사전 공지, Google 별도 고지 및 이전 공개본을 제공합니다. 한도 적용은 공지된 시행일 이후 시작합니다.
- Docker를 복구하고 별도 PostgreSQL 17 Supabase에서 신규 마이그레이션과 전체 SQL 검사를 검증합니다.
- 배포: 새 마이그레이션 3개, MCP Edge 함수와 웹을 함께 올립니다. 운영자 권한과 한도 시행 시각은 확인한 운영 설정으로 별도 지정합니다.

## 0.70.2 — 2026-10-24

The research library's latest edits now continue past the first eight: a More button under the list opens twenty older records at a time, newest first, and the heading shows how many of how many are listed. The keyboard moves on to the first record that opened. The list starts again from eight when the project or the search words change. Nothing new is loaded; the records are the ones the app already holds.

- '모든 기록' 화면의 '최근 수정한 기록'이 8개에서 멈추던 것을 고쳤습니다. 목록 아래 '더 보기'를 누를 때마다 20개씩 더 보이고, 제목 줄 오른쪽에 '31개 중 8개'처럼 개수가 나옵니다.
- '더 보기'를 누르면 새로 열린 첫 기록으로 키보드 초점이 옮겨 가서, 읽던 곳에서 이어 볼 수 있습니다.
- 프로젝트를 바꾸거나 검색어를 바꾸면 다시 8개부터 보입니다. 이미 불러온 기록 목록이라 펼칠 때 페이지를 새로 받지 않습니다.
- 배포: 마이그레이션과 MCP 함수 변경은 없습니다. 사이트만 다시 올립니다.

## 0.70.1 — 2026-10-24

Bold and italics now close before Korean, Japanese and Chinese text even right after a parenthesis or quote, so **활용(exploitation)**이다 renders bold instead of showing its asterisks. Pages, notes, the editor and the plugin panel read Markdown with the CJK-friendly rule, and saved pages need no edit. The writing guide (43) now asks AIs to mark each section's one answer or decision as its key sentence, within the same limits.

- 괄호나 따옴표로 끝나는 굵은 글 바로 뒤에 조사가 붙으면 별표(**)가 그대로 보이던 문제를 고쳤습니다. 예: `**활용(exploitation)**이다`. 페이지, 노트, 편집기, 플러그인 패널이 한·중·일 문장에 맞춘 규칙으로 읽고, 영어 문장은 지금과 같습니다. 저장된 글은 고치지 않아도 굵게 보입니다.
- AI가 중요한 문장을 거의 칠하지 않던 문제: 쓰기 지침 43이 절마다 답이나 결정이 있으면 그 문장을 핵심(형광펜)으로 칠하라고 안내하고, 검토 단계에서 확인합니다. 한도(절마다 핵심 1개, 강조 3개)와 서버 검사는 그대로입니다.
- 배포: 마이그레이션은 없습니다. MCP 함수(지침, 패널)와 사이트를 다시 올립니다.

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
