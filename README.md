# Research Loop plugin

프로젝트 · 연구 페이지 · 실험 · 문헌 · 일정 · 마감 · AI 작업

[Research Loop](https://research-loop.lukeo112.chatgpt.site/)에 Codex·Claude Code를 연결하는 플러그인입니다. 웹앱 소스와 연구 데이터는 포함하지 않습니다. GitHub 배포와 OpenAI Plugins Directory 심사·게시는 별개이며, Directory에는 아직 게시되지 않았습니다.

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

## Claude Code 설치

```sh
claude plugin marketplace add jeongseokO/Research-Loop-Plugin
claude plugin install research-loop@research-loop
```

새 세션에서 `/mcp`를 열어 Research Loop OAuth 로그인을 완료합니다. 기존 수동 MCP 연결이 있다면 중복 연결하지 말고 사용할 연결을 확인하세요. 설치는 서버 접근 승인을 대신하지 않습니다.

## 업데이트

현재 패키지: **0.4.4**. “Research Loop를 최신화해줘”를 요청하면 확인된 변화부터 기존 기록·관련 질문·읽는 순서에 반영하도록 안내합니다. 바뀐 내용이 없으면 문서를 고치지 않고, 반영·승인 대기·미확인을 구분합니다. 그림 밖 캡션, 충분한 문헌 설명, 권한·검토 규칙과 필요한 안내만 읽는 방식을 유지합니다.

```sh
codex plugin marketplace upgrade research-loop
codex plugin add research-loop@research-loop
```

Claude Code는 `claude plugin marketplace update research-loop` 후 `claude plugin update research-loop@research-loop`를 실행합니다.

업데이트 후 새 작업을 시작합니다. 실제 계정의 설치·OAuth·권한 검증 상태는 [배포 체크리스트](RELEASE-CHECKLIST.md)를 참고하세요.

MCP 서버의 도구·작성 규격은 연결된 서버에서 제공됩니다. 플러그인은 해당 작업에 필요한 안내만 읽도록 연결하며, 매번 전체 이력이나 모든 가이드를 불러오지 않습니다. 서버 업데이트가 이미 설치된 플러그인 파일까지 교체하지는 않습니다. 위 절차는 공개판용이며, 개인용 `research-loop@personal`은 해당 로컬 원본을 갱신한 뒤 재설치해야 합니다.

하이라이트에서 보낸 AI 요청은 선택 문장과 요청사항을 함께 전달합니다. AI는 원문을 다시 확인하고 담당 작업을 claim한 뒤 처리합니다. 큐에 추가하는 것만으로 Codex·Claude가 자동 실행되지는 않습니다.

## 방법론 그림

“이 방법론을 overview figure로 그려서 페이지에 넣어줘”라고 요청합니다. 그림 작업에만 [method-figure 스킬](plugins/research-loop/skills/method-figure/SKILL.md)을 읽습니다.

- 검증된 방법을 토큰·tensor·cache·연산·연결로 표현합니다. 설명은 그림 밖에 둡니다.
- 로컬 Python·Matplotlib으로 PNG와 SVG/PDF, 수정용 JSON을 만듭니다. 별도 이미지 생성 API는 사용하지 않습니다. 환경이 없으면 [전용 환경 설정](plugins/research-loop/skills/method-figure/references/setup.md)이 필요합니다.
- AI가 실제 이미지를 확인하고 페이지에 첨부합니다. 코드만 작성·파일만 업로드한 상태와 승인 대기를 완료로 보고하지 않습니다.
- 원본 파일은 로컬 작업 폴더에 유지합니다. 웹앱에는 PNG를 넣습니다. 그림의 정확성·가독성은 AI와 연구자가 확인해야 하며 모든 모델의 실행을 보장하지는 않습니다.

MCP만 연결하면 로컬 스킬·제작 스크립트가 설치되지는 않습니다. 플러그인을 갱신하거나 사용 가능한 별도 그림 도구가 필요합니다.

## 권한과 지원 범위

사용자와 AI를 확인하고 프로젝트·페이지의 현재 revision을 읽은 뒤 요청된 변경만 수행합니다. Editor AI는 본인 사용자 계정이 처음 만든 일반 노트(토론 제외)·문헌·실험·데이터셋·결과를 직접 수정할 수 있습니다. 다른 사람의 기록과 질문·방법·주장 등 보호된 기록, 마감, 휴지통·복원, 링크·프로젝트 정보·주간 계획 변경은 검토 요청입니다. 기존 계획의 상태만 작성자 또는 수락한 담당자가 직접 바꿀 수 있으며 보관·복원은 제외됩니다. 새 기록·토론·답글은 직접 생성하지만 새 마감은 검토가 필요합니다. 작성자는 생성 이력으로 확인하며 속성 편집으로 권한이 바뀌지 않습니다. 직접 수정에는 write, 보호된 수정에는 write와 propose 권한이 필요합니다. 승인된 Semi-Owner AI는 허용된 연구 내용을 직접 수정하며, 프로젝트 생애·접근 권한 관리는 Owner에게 남습니다. Viewer AI는 읽기 전용입니다. 서버가 제안으로 처리한 변경은 승인 전까지 반영되지 않습니다.

표와 문서 블록, Markdown 강조를 지원합니다. AI가 실험 데이터로 직접 plot·figure를 그린 뒤 PNG/JPEG/WebP/GIF 파일을 업로드하고 페이지에 넣을 수 있습니다. 하루 업로드 개수 제한 없이 파일당 최대 10MiB이며, SVG/PDF 그림은 PNG로 내보냅니다. 그림 생성은 연결한 AI의 실행·이미지 도구가 담당하고, Research Loop는 검증된 파일을 저장합니다.

작은 파일은 MCP에서 직접 업로드할 수 있고, 큰 파일은 임시 업로드 주소를 사용합니다. 페이지 저장 권한과 Owner 검토 절차는 그대로 유지됩니다. 업로드·다운로드용 임시 주소를 페이지에 저장하거나 공개하지 마세요.

Google Calendar 연결 및 프로젝트 선택은 웹앱의 개인 설정에서 수행합니다. MCP/AI는 Google OAuth 토큰에 접근하지 못하며, Calendar 연결·계정 관리 권한을 갖지 않습니다.

## 문의

게시자: 오정석 · [지원 이메일](mailto:jeongseok0112@gmail.com) · [문제 신고](https://github.com/jeongseokO/Research-Loop-Plugin/issues)

공개 이슈나 이메일에 API 키, OAuth 토큰, 비밀번호, 비공개 연구 내용을 첨부하지 마세요. 계정 관련 문의는 지원 이메일로 요청하세요.

별도 오픈소스 라이선스는 아직 지정하지 않았습니다. 공개 열람 가능 여부와 재사용 허가는 구분됩니다.
