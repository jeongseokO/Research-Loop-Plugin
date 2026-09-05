# Research Loop plugin

프로젝트 · 연구 페이지 · 실험 · 문헌 · 일정 · 마감 · AI 작업

[Research Loop](https://research-loop.lukeo112.chatgpt.site/)에 Codex를 연결하는 플러그인입니다. 웹앱 소스와 연구 데이터는 포함하지 않습니다. GitHub 배포와 OpenAI Plugins Directory 심사·게시는 별개이며, Directory에는 아직 게시되지 않았습니다.

## Codex 설치

플러그인을 지원하는 최신 Codex에서 다음 명령을 실행합니다.

```sh
codex plugin marketplace add jeongseokO/Research-Loop-Plugin
codex plugin add research-loop@research-loop
```

새 작업에서 Research Loop 계정으로 로그인하고 권한을 승인합니다. API 키를 채팅에 붙일 필요가 없습니다. 연결 시 자동 OAuth 등록이 지원되지 않으면 다음 명령을 한 번 실행합니다.

```sh
codex mcp login research-loop-plugin --scopes email --oauth-client-registration dcr
```

사용 예:

- “내 Research Loop 프로젝트 현황을 보여줘.”
- “이 실험 결과를 기존 페이지에 표로 추가해줘.”
- “이 프로젝트의 마감을 확인하고 다음 주 계획을 만들어줘.”

기존 개인용 `research-loop@personal`을 사용 중이라면 두 플러그인을 동시에 켜지 마세요. 공개판의 연결을 확인한 뒤 기존 개인용 플러그인을 해제합니다. 이 저장소는 기존 설치나 API 키를 자동 변경하지 않습니다.

## 업데이트

```sh
codex plugin marketplace upgrade research-loop
codex plugin add research-loop@research-loop
```

업데이트 후 새 작업을 시작합니다. 실제 계정의 설치·OAuth·권한 검증 상태는 [배포 체크리스트](RELEASE-CHECKLIST.md)를 참고하세요.

## 권한과 지원 범위

사용자와 AI를 확인하고 프로젝트·페이지의 현재 revision을 읽은 뒤 요청된 변경만 수행합니다. Editor AI의 보호된 수정은 Owner 검토 요청으로 제출됩니다. Viewer AI는 읽기 전용입니다.

표와 문서 블록, Markdown 강조를 지원합니다. AI가 실험 데이터로 직접 plot·figure를 그린 뒤 PNG/JPEG/WebP/GIF 파일을 업로드하고 페이지에 넣을 수 있습니다. 파일당 최대 10MiB, 사용자당 하루 64개이며 SVG/PDF 그림은 PNG로 내보냅니다. 그림 생성은 연결한 AI의 실행·이미지 도구가 담당하고, Research Loop는 검증된 파일을 저장합니다.

작은 파일은 MCP에서 직접 업로드할 수 있고, 큰 파일은 임시 업로드 주소를 사용합니다. 페이지 저장 권한과 Owner 검토 절차는 그대로 유지됩니다. 업로드·다운로드용 임시 주소를 페이지에 저장하거나 공개하지 마세요.

Google Calendar 연결 및 프로젝트 선택은 웹앱의 개인 설정에서 수행합니다. MCP/AI는 Google OAuth 토큰에 접근하지 못하며, Calendar 연결·계정 관리 권한을 갖지 않습니다.

## 문의

게시자: 오정석 · [지원 이메일](mailto:jeongseok0112@gmail.com) · [문제 신고](https://github.com/jeongseokO/Research-Loop-Plugin/issues)

공개 이슈나 이메일에 API 키, OAuth 토큰, 비밀번호, 비공개 연구 내용을 첨부하지 마세요. 계정 관련 문의는 지원 이메일로 요청하세요.

별도 오픈소스 라이선스는 아직 지정하지 않았습니다. 공개 열람 가능 여부와 재사용 허가는 구분됩니다.
