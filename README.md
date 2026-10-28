# Research Loop plugin

[Research Loop](https://airesearchloop.com/)에 Claude·Claude Code·Codex·ChatGPT를 연결하는 플러그인입니다. AI가 연구 페이지를 읽고 쓰고, 저장소에서 돌린 실험을 기록하고, 방법을 단계별 도해로 설명하고, 팀이 맡긴 AI 요청을 처리합니다. 웹앱 소스와 연구 데이터는 들어 있지 않습니다.

## 설치

**Claude (웹·데스크톱·모바일·Cowork)**

1. **Customize → Connectors**에서 **Add custom connector**: 이름 Research Loop, 주소 `https://airesearchloop.com/mcp`(등록 방식을 물으면 **Register automatically**). Research Loop 계정으로 로그인합니다.
2. **Customize → Plugins**에서 **Add → Add marketplace**: `jeongseokO/Research-Loop-Plugin`을 넣고 Research Loop를 설치합니다.

같은 Claude 계정으로 로그인한 Claude Code에는 다음 실행부터 플러그인이 따라옵니다. `/mcp`에서 `plugin:research-loop:research`를 한 번 인증합니다.

**Claude Code (API 키로 쓰거나 터미널에서 설치)**

```sh
claude plugin marketplace add jeongseokO/Research-Loop-Plugin
claude plugin install research-loop@research-loop
```

Claude Code를 다시 시작하고 대화창에서 `/mcp` → Research Loop → 인증을 눌러 본인 계정으로 로그인합니다.

**Codex · ChatGPT · MCP만 연결**은 [AI 연결 안내](CONNECTION-GUIDE.md)를 따르세요 ([English](CONNECTION-GUIDE.en.md)). Codex에서는 플러그인과 MCP 직접 연결 중 하나만 씁니다. 설치는 프로젝트 접근 승인을 대신하지 않습니다.

## Claude Code 명령

| 명령 | 하는 일 |
| --- | --- |
| `/research-loop:brief` | 프로젝트의 현재 답과 불확실한 점, 내 할 일과 다음 단계, 검토 대기, 나에게 온 질문을 읽기만 해서 요약합니다. |
| `/research-loop:record` | 이 저장소에서 돌린 실험을 실험 페이지로 기록합니다. 결과 파일의 값 그대로 실행 목록·설정·결과 표(그래프 포함)·핵심 결론을 씁니다. |
| `/research-loop:explain` | 코드에 있는 방법을 읽고 방법론 페이지의 `작동 원리`에 단계별 도해로 그립니다. |
| `/research-loop:task` | 이 연결에 들어온 AI 요청 하나를 선점해 처리하고 검토 대기로 넘깁니다. |

**저장소 연결.** 저장소 맨 위에 `.research-loop.json`을 두면 명령이 어느 프로젝트에 기록할지 묻지 않습니다. 처음 프로젝트를 알려 주면 AI가 만들어 줍니다. 자격 증명은 들어가지 않아 커밋해도 됩니다.

```json
{ "project": "proj-kv", "name": "KV cache 예산" }
```

명령 없이 “이 실험 결과를 Research Loop에 기록해줘”처럼 말해도 같은 지침을 따릅니다.

## 페이지가 직접 그리는 그림

- **표 → 그래프.** 측정값 비교는 표를 그대로 두고 `table.chart`로 읽는 방식을 정합니다. 앱이 표의 값으로 그래프를 그리므로 그림과 숫자가 어긋나지 않고, 사람은 표를 고치면 됩니다.
- **도해.** 방법의 작동 원리나 실험 설계는 부품·연결·단계를 데이터로 적은 도해 블록으로 남깁니다. 앱이 배치해 그리고 단계마다 넘겨 볼 수 있으며, 발표 자료로 바꾸면 같은 도해가 단계 장면이 됩니다.
- **이미지 파일**은 표나 도해로 담을 수 없을 때만 만듭니다. 분포·히트맵은 [research-plot](plugins/research-loop/skills/research-plot/SKILL.md), 논문·슬라이드용 정적 구조도는 [method-figure](plugins/research-loop/skills/method-figure/SKILL.md) 스킬을 씁니다. 수치를 이미지 생성 모델로 그리지 않고, 설명은 그림 밖 캡션에 둡니다. MCP만 연결하면 이 로컬 스크립트는 설치되지 않습니다.

## 업데이트

Claude 앱은 플러그인을 가져온 마켓플레이스에서 새 버전을 확인합니다(바로 받으려면 Customize → Plugins에서 마켓플레이스의 Update). Codex는 시작할 때 새 버전을 받습니다. Claude Code는 대화창의 `/plugin` → Marketplaces → research-loop에서 자동 업데이트(Enable auto-update)를 한 번 켜 둡니다. 새 버전은 다시 연 뒤 새 대화부터 적용됩니다. 업데이트하려고 다시 설치하지 마세요. VS Code나 앱에서 설치하면 로그인을 새로 하게 되고 'AI 연결'에 연결이 하나 더 생깁니다.

현재 패키지: **0.92.0** — 웹사이트·MCP 서버·패널과 같은 번호입니다. 무엇이 바뀌었는지는 [변경 내역](CHANGELOG.md)에 있습니다.

## 공유 서버에서 사용

최신화는 전체 데이터·로그 재검색이나 그림 일괄 재생성을 뜻하지 않습니다. 기존 결과를 재사용하고 필요한 작업만 순서대로 실행합니다.

- 그림 실행기: 기본 60초, 최대 120초, 같은 사용자의 동시 실행 거절, 수치 라이브러리 스레드 1개. 직접 작성한 plot 스크립트는 [실행기](plugins/research-loop/scripts/render_guard.py)로 실행합니다.
- 출력: plot 최대 12 MP·240–600 DPI, 방법론 그림 최대 8 MP. 업로드는 파일당 10 MiB입니다.
- 실행기는 OS의 CPU·메모리 할당량이 아닙니다. 여러 사용자의 총 부하는 서버 관리자의 제한도 필요합니다. 한도를 넘으면 작업을 나누고 같은 작업을 병렬로 다시 시도하지 않습니다.

## 권한

AI는 연결된 사람의 권한 안에서만 움직입니다. 현재 판(revision)을 읽고 요청된 변경만 저장합니다.

- **Editor AI**는 자기 사람이 처음 만든 일반 노트·문헌·실험·데이터셋·결과를 직접 고칩니다. 다른 사람의 기록, 질문·방법·주장, 마감, 링크, 프로젝트 정보, 주간 계획 변경은 검토 요청이 되고 승인 전에는 반영되지 않습니다.
- **Semi-Owner AI**는 허용된 연구 내용을 직접 고칩니다. 프로젝트 삭제·접근 권한은 Owner에게 남습니다. **Viewer AI**는 읽기만 합니다.
- 작성자는 생성 이력으로 판정하며 속성을 고쳐도 바뀌지 않습니다. 업로드·다운로드 임시 주소는 페이지에 저장하거나 공유하지 않습니다.
- Google Calendar 연결은 웹앱의 개인 설정에서 합니다. AI는 Google 토큰에 접근하지 못합니다.

## 문의

게시자: 오정석 · [지원 이메일](mailto:jeongseok0112@gmail.com) · [문제 신고](https://github.com/jeongseokO/Research-Loop-Plugin/issues)
