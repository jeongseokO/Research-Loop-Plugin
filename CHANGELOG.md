# 변경 내역

Research Loop는 버전이 하나입니다. 웹사이트, MCP 서버, ChatGPT·Claude 안의 패널, 이 플러그인 패키지가 같은 번호를 씁니다. 새 버전은 맨 위에 `## x.y.z` 항목으로 적습니다. 항목의 첫 문단은 플러그인 디렉터리에 올라가는 release note이므로 영어 한 문단으로 쓰고, 그 아래에 사람이 읽을 내용을 한국어로 적습니다. 릴리스 명령이 제목에 날짜를 붙입니다.

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
