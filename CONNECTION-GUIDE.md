# AI 연결 안내

처음 연결한다면 **Codex 또는 Claude Code 플러그인**을 권장합니다. 사용하는 도구의 절차 하나만 따라가세요.

| 연결 방식 | 포함되는 것 | API 키 발급 |
| --- | --- | --- |
| 플러그인 | MCP 연결 + 작업별 지침 + 그림 제작 도구 | 불필요 · Research Loop 로그인 |
| MCP 직접 연결 | 연구 조회·편집 도구와 서버 지침 | OAuth 지원 시 불필요 |
| API 키 연결 | OAuth를 지원하지 않는 도구의 호환 연결 | 필요 |

플러그인을 설치했다면 같은 MCP를 따로 추가하지 마세요. 하나의 AI 연결로 허가받은 여러 프로젝트에 접근할 수 있습니다.

## 1. 시작 전 준비

1. [Research Loop](https://research-loop.lukeo112.chatgpt.site/)에 **본인 계정**으로 로그인합니다.
2. 사용할 프로젝트를 만들거나, 받은 초대를 수락합니다.
3. 사용할 Codex 또는 Claude Code에 로그인합니다. AI 서비스 구독과 Research Loop 계정 연결은 별개입니다.

동료와 계정·API 키를 공유하지 않습니다. 각자 연결해야 누가 어떤 AI로 작업했는지 기록됩니다. 일반 사용자는 Supabase나 Google Cloud 관리자 설정을 할 필요가 없습니다.

## 2. Codex · VS Code 플러그인

### 화면에서 설치

1. VS Code의 Codex 확장에서 **플러그인 → 플러그인 마켓플레이스 추가**를 엽니다. 메뉴 이름은 버전에 따라 다를 수 있습니다.
2. 아래 세 칸을 입력합니다.

| 항목 | 입력값 |
| --- | --- |
| 출처 | `https://github.com/jeongseokO/Research-Loop-Plugin.git` |
| Git ref | `codex/public-release` |
| Sparse 경로 | **비워두기** |

3. 추가한 마켓플레이스에서 초록색 루프 아이콘의 **Research Loop**를 선택해 설치합니다.
4. 계정 연결 창이 열리면 Research Loop에 로그인하고, 연결할 AI 이름·권한을 확인해 승인합니다.
5. Codex를 다시 열고 **새 대화**에서 “Research Loop에 연결된 내 계정과 접근 가능한 프로젝트를 확인해줘”라고 요청합니다.

**연결 확인:** 본인 이름과 예상한 프로젝트가 나오면 정상입니다. 팀 프로젝트가 없다면 아래 ‘프로젝트 접근 권한’을 확인하세요.

### 터미널로 설치하는 경우

위 화면 대신, 플러그인을 지원하는 Codex CLI가 설치된 터미널에서 실행합니다. 화면 설치와 둘 다 할 필요는 없습니다.

```sh
codex plugin marketplace add jeongseokO/Research-Loop-Plugin --ref codex/public-release
codex plugin add research-loop@research-loop
```

로그인 창이 열리지 않으면 다음 명령으로 연결합니다. 플러그인의 서버 이름은 `research-loop-plugin`입니다.

```sh
codex mcp login research-loop-plugin --scopes email --oauth-client-registration dcr
```

**VS Code Remote SSH 사용 시:** 로컬 컴퓨터와 원격 서버의 설치·로그인은 서로 다를 수 있습니다. Codex가 실행되는 환경에서 설치하고, `/mcp` 등 해당 환경의 연결 목록을 확인하세요. 로그인 후 `127.0.0.1` 연결 오류가 나면 API 키를 반복 발급하지 말고, 실제 callback 주소의 포트를 로컬 브라우저에서 해당 환경으로 전달할 수 있는지 확인합니다. 고정 포트를 임의로 추측하지 마세요. 조직 관리 설정이 설치를 막는다면 관리자에게 문의합니다.

설치 형식과 명령은 [OpenAI 플러그인 문서](https://developers.openai.com/plugins/build/plugins), 원격 연결·OAuth는 [Codex MCP 문서](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)를 참고합니다.

## 3. Claude Code 플러그인

1. Claude Code를 사용하는 터미널에서 아래 명령을 차례로 실행합니다.

```sh
claude plugin marketplace add jeongseokO/Research-Loop-Plugin
claude plugin install research-loop@research-loop
```

2. Claude Code를 다시 시작합니다.
3. 대화 입력창에 `/mcp`를 입력하고 Research Loop 연결의 인증 항목을 선택합니다.
4. 브라우저에서 **본인 Research Loop 계정**으로 로그인하고 연결을 승인합니다.
5. 새 대화에서 “Research Loop의 내 계정과 접근 가능한 프로젝트를 확인해줘”라고 요청합니다.

일반 터미널에서는 `claude ...` 명령을, Claude Code 대화 입력창에서는 `/mcp`를 사용합니다. Claude 웹·데스크톱의 커넥터와 Claude Code 플러그인은 설치 방식이 다릅니다. [Claude Code 공식 플러그인 안내](https://code.claude.com/docs/en/discover-plugins)

## 4. 플러그인 없이 MCP만 연결

이미 플러그인으로 연결했다면 이 단계는 건너뜁니다. MCP만 연결해도 연구 페이지를 읽고 편집할 수 있지만, 플러그인의 로컬 그림 제작 스크립트까지 설치되지는 않습니다.

**서버 주소 · Streamable HTTP**

```text
https://ezmkpdnchcpjuvpilpxu.supabase.co/functions/v1/research-loop-mcp
```

### Codex

1. Codex CLI가 설치된 터미널에서 서버를 추가합니다.

```sh
codex mcp add research-loop --url https://ezmkpdnchcpjuvpilpxu.supabase.co/functions/v1/research-loop-mcp
codex mcp login research-loop --scopes email --oauth-client-registration dcr
```

2. 브라우저에서 Research Loop 계정 연결을 승인합니다.
3. 새 대화에서 계정과 프로젝트를 확인합니다. 직접 연결의 서버 이름은 `research-loop`이며, 플러그인의 `research-loop-plugin`과 구분합니다.

### Claude Code

1. 터미널에서 다음 명령을 실행합니다.

```sh
claude mcp add --transport http --scope user research-loop https://ezmkpdnchcpjuvpilpxu.supabase.co/functions/v1/research-loop-mcp
```

2. Claude Code의 `/mcp`에서 Research Loop를 선택하고 인증합니다.
3. 본인 계정과 프로젝트가 보이는지 확인합니다. [Claude Code MCP 안내](https://code.claude.com/docs/en/mcp)

### Claude 웹·데스크톱 / 다른 MCP 도구

1. 도구의 커넥터·MCP 설정에서 새 원격 연결을 추가합니다. 해당 메뉴의 제공 여부는 플랜·조직 정책에 따라 다릅니다.
2. 이름을 **Research Loop**, 서버 주소를 위 주소로 입력합니다. 전송 방식을 고르는 경우 **Streamable HTTP**를 선택합니다.
3. 연결·인증을 눌러 Research Loop 계정으로 로그인합니다. 앱 주소나 GitHub 저장소 주소를 MCP 서버 칸에 넣지 않습니다.
4. 계정과 접근 가능한 프로젝트를 확인합니다. OAuth를 지원하지 않는 도구만 아래 API 키 절차를 사용합니다.

## 5. 프로젝트 접근 권한

1. Research Loop 웹앱의 **내 AI**를 엽니다.
2. 방금 연결한 AI 이름을 찾아 프로젝트별 접근 상태를 확인합니다.
3. **본인이 Owner인 프로젝트:** 별도 요청 없이 접근할 수 있습니다.
4. **초대받은 프로젝트:** 해당 AI에서 **접근 요청**을 누릅니다. 프로젝트 Owner가 승인한 뒤 사용할 수 있습니다. 사람의 초대 수락만으로 AI 접근까지 승인되지는 않습니다.
5. 승인 후 AI에게 프로젝트 목록을 다시 확인하도록 요청합니다. 키를 새로 발급할 필요는 없습니다.

AI의 실제 권한은 **내 기능 권한 × 내 프로젝트 역할 × 승인된 AI 접근 범위** 안에서 정해집니다. 승인 요청으로 처리된 편집은 Owner 등 검토 권한자가 승인하기 전까지 적용되지 않습니다.

## 6. API 키가 필요한 경우만

OAuth로 연결했다면 이 단계는 필요 없습니다. 여기서 말하는 키는 OpenAI·Anthropic API 키가 아니라 **Research Loop 접속용 키**입니다.

1. 웹앱 **내 AI → API 키 · 호환 연결**을 엽니다.
2. AI 이름·클라이언트·필요한 기능 권한·만료일을 선택하고 키를 발급합니다.
3. 한 번만 표시되는 키를 본인의 안전한 비밀 저장소에 보관합니다. 채팅·노트·Git 저장소에 붙이지 않습니다.
4. 같은 화면에서 사용하는 도구의 **Codex / Claude 설정 복사**를 누릅니다. 기본 환경 변수 이름은 `RESEARCH_LOOP_API_KEY`입니다.
5. 복사한 설정을 해당 도구의 MCP 설정에 넣고, **AI가 실행되는 환경**에서 그 환경 변수에 키를 제공합니다. 키를 설정 파일에 평문으로 넣지 마세요. VS Code는 다른 터미널에서 설정한 환경 변수를 자동으로 받지 않을 수 있습니다.
6. 도구를 다시 시작하고 연결을 확인한 뒤, 필요한 프로젝트 접근을 요청합니다.

API 키가 노출됐거나 더 쓰지 않는 AI는 **내 AI → AI 삭제**로 제거하고 필요한 연결만 다시 만듭니다. 삭제하면 해당 AI 연결은 더 이상 사용할 수 없습니다.

## 7. 업데이트와 중복 연결 정리

MCP 서버 지침은 서버에서 제공되지만, 설치된 플러그인 파일·아이콘은 별도로 업데이트해야 합니다.

**Codex CLI**

```sh
codex plugin marketplace upgrade research-loop
codex plugin add research-loop@research-loop
```

**Claude Code 터미널**

```sh
claude plugin marketplace update research-loop
claude plugin update research-loop@research-loop
```

업데이트 후 도구를 다시 열고 새 대화를 시작합니다. 개인용 `research-loop@personal`이나 수동 MCP 연결이 함께 있다면, 새 연결이 작동하는지 확인한 뒤 옛 연결을 비활성화하세요. 작동 중인 연결을 확인 없이 먼저 지우지 않습니다.

## 8. 연결이 안 될 때

| 증상 | 먼저 확인할 것 |
| --- | --- |
| 마켓플레이스에 플러그인이 없음 | 저장소 주소·Git ref 확인 → Sparse 비우기 → 마켓플레이스 갱신 |
| 플러그인 메뉴·명령이 없음 | 해당 Codex/Claude Code 버전의 플러그인 지원 여부와 조직 정책 확인. 미지원이면 MCP 직접 연결 사용 |
| 로그인 후 프로젝트가 안 보임 | 로그인 계정 → 사람의 프로젝트 초대 수락 → 해당 AI의 프로젝트 접근 승인 순서로 확인 |
| 편집했는데 반영되지 않음 | AI가 ‘적용 완료’가 아니라 ‘검토 요청’을 보냈는지 확인 → 알림에서 요청 확인 |
| `instructions_required` | AI가 현재 프로젝트 작업 지침을 다시 읽은 뒤, 여전히 필요한 작업만 재시도 |
| 서비스 계정 연결 설정 누락 | 서비스 운영 설정 문제. 사용자에게 Supabase 설정이나 반복 키 발급을 요구하지 말고 관리자에게 문의 |
| 옛 지침·아이콘이 계속 보임 | 플러그인 갱신 → Codex/Claude Code 재시작 → 새 대화. 기존 대화의 지침은 남을 수 있음 |

문의할 때는 사용한 도구·버전, 실패한 단계, 오류 문구를 알려주세요. API 키·OAuth 토큰·비밀번호·비공개 연구 내용은 보내지 마세요. [지원 문의](mailto:jeongseok0112@gmail.com)
