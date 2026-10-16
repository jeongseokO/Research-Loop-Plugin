# 변경 내역

Research Loop는 버전이 하나입니다. 웹사이트, MCP 서버, ChatGPT·Claude 안의 패널, 이 플러그인 패키지가 같은 번호를 씁니다. 새 버전은 맨 위에 `## x.y.z` 항목으로 적습니다. 항목의 첫 문단은 플러그인 디렉터리에 올라가는 release note이므로 영어 한 문단으로 쓰고, 그 아래에 사람이 읽을 내용을 한국어로 적습니다. 릴리스 명령이 제목에 날짜를 붙입니다.

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
