# 05. Codex CLI 설치 가이드

---

## 0. 설치 전에 알아둘 것

OpenAI **Codex CLI**는 터미널에서 돌아가는 **AI 코딩 에이전트 CLI**입니다. Claude Code와 역할이 같지만, 인증·모델·설정 파일이 전부 다른 생태계를 씁니다. 핵심 차이를 먼저 정리하면 다음과 같습니다.

| 항목 | Claude Code | Codex CLI |
|------|-------------|-----------|
| 공식 CLI 명령어 | `claude` | `codex` |
| 설치 패키지 (npm) | `@anthropic-ai/claude-code` | `@openai/codex` |
| 설치 패키지 (Homebrew) | `claude-code` | `codex` |
| 인증 | Anthropic 계정 (Claude Pro/Max) 또는 API 키 | ChatGPT 계정 (Plus/Pro/Business/Enterprise) 또는 `OPENAI_API_KEY` |
| Desktop 앱 연동 | Claude Desktop 앱 (Mac/Windows) | Codex Desktop 앱 (**macOS 전용, 2026-04 기준**) · 브라우저 Codex는 전 OS |
| 설정 파일 위치 | `~/.claude/settings.json` | `~/.codex/config.toml` |
| 설정 포맷 | JSON | TOML |
| 비대화형(CI) 모드 | `claude -p "..."` | `codex exec "..."` |
| 공식 저장소 | github.com/anthropics/claude-code | github.com/openai/codex |

> **핵심 포인트.** 두 도구는 "같은 컴퓨터에 공존 가능"합니다. 경로가 완전히 다르고(`~/.claude` vs `~/.codex`) 명령어가 다르기 때문입니다. 이 과정 전체는 두 도구를 **같은 폴더에서 번갈아 쓰며 비교**하는 흐름으로 설계돼 있으므로, 둘 다 설치해 두는 것을 권장합니다.

설치 방식은 세 가지입니다.

| 방식 | 장점 | 추천 대상 |
|------|------|-----------|
| **0. Codex Desktop 앱 (GUI, Mac 전용) / 브라우저 Codex (Windows·Linux)** | 설치 파일 더블 클릭 또는 웹 접속으로 끝. Codex를 GUI로 바로 체험 | 터미널이 처음이라 부담스러운 분 |
| **A. 네이티브 CLI 설치 (권장)** | 가장 공식적인 경로. Homebrew(Mac)·npm·공식 바이너리 | 이 교재의 본 실습을 하실 분 |
| **B. 바이너리 직접 내려받기** | Node.js·Homebrew·npm 어느 것도 쓰고 싶지 않을 때 | 회사 보안 정책으로 패키지 매니저 사용이 제한된 분 |

**세 방식을 동시에 설치하지 마세요.** 단, 방식 0과 A는 **병행 가능**합니다 — 앱에서 ChatGPT로 로그인해 두면 CLI가 그 인증 정보를 그대로 재사용합니다.

---

## 방식 0. GUI로 빠르게 시작하기 (Mac = 앱 / Windows·Linux = 브라우저 Codex)

> **중요 — 플랫폼별로 경로가 다릅니다.**
> - **macOS:** 전용 **Codex Desktop 앱**을 내려받습니다(아래 0-1A).
> - **Windows / Linux:** Codex Desktop 앱은 **2026-04 기준 macOS 전용**이라 제공되지 않습니다. 대신 **브라우저 Codex**([https://chatgpt.com/codex](https://chatgpt.com/codex))를 GUI 대체로 사용합니다(아래 0-1B).
>
> 두 경로 모두 "GUI 맛보기"라는 목적은 같고, 본 실습의 주 무대는 여전히 방식 A(CLI)입니다.

### 0-1A. macOS — Codex Desktop 앱 다운로드

> 일반 ChatGPT 앱이 아니라 **Codex 전용 Desktop 앱**을 받아야 합니다. 둘은 다른 앱입니다. ChatGPT 앱은 범용 대화 UI이고, Codex 앱은 로컬 저장소를 대상으로 한 **에이전트 작업 전용 UI**(작업 큐, 샌드박스 정책, diff 리뷰, PR 생성)에 최적화돼 있습니다.

1. 브라우저에서 **Codex 제품 페이지**([https://chatgpt.com/codex](https://chatgpt.com/codex) 또는 [https://openai.com/codex](https://openai.com/codex))에 접속.
2. 화면에서 **Download the Codex desktop app (macOS)** 또는 "Download for Mac" 버튼을 눌러 `.dmg` 파일을 내려받습니다.
3. 더블 클릭해 Codex 아이콘을 Applications 폴더로 드래그.
4. Applications에서 Codex를 실행하고 **ChatGPT 계정(Plus / Pro / Business / Enterprise)** 으로 로그인. 계정 주체는 ChatGPT지만 로그인 후 열리는 UI는 Codex 전용입니다.

> 공식 다운로드 경로가 바뀌는 일이 잦습니다. 위 링크에서 버튼이 보이지 않으면 상단 네비게이션의 "Codex" 메뉴나 문서 페이지에서 Download를 찾으세요.

### 0-1B. Windows · Linux — 브라우저 Codex로 시작하기

Windows·Linux에는 전용 Desktop 앱이 없으므로 **웹 기반 Codex**를 쓰면 됩니다. 설치 없이 브라우저만으로 동일한 에이전트 기능을 체험할 수 있습니다.

1. 브라우저(Chrome·Edge·Firefox 등)에서 [https://chatgpt.com/codex](https://chatgpt.com/codex) 접속.
2. ChatGPT 계정(Plus / Pro / Business / Enterprise)으로 로그인.
3. 우측 상단 **+ New task** 또는 **Connect a repo**로 시작. GitHub 저장소를 연결하거나, 샘플 저장소를 열어 에이전트에게 작업을 지시할 수 있습니다.

> **브라우저 Codex와 Desktop 앱의 차이 — 반드시 알아둘 것.**
> - **브라우저 Codex는 OpenAI의 클라우드 샌드박스에서 실행**됩니다. 즉 내 로컬 폴더에는 직접 접근하지 못합니다. 파일 변경은 **GitHub 저장소를 통한 PR** 형태로만 내 환경에 반영됩니다.
> - **Desktop 앱은 로컬 폴더를 직접 연다**는 점이 가장 큰 차이입니다.
> - 이 과정의 뒷 단원은 **로컬 Git 실습**을 전제하므로, Windows·Linux 학습자는 0-1B로 맛만 본 뒤 **방식 A(CLI)로 빠르게 넘어가는 것**을 권장합니다.

### 0-2. GUI 둘러보기

#### macOS — Codex Desktop 앱

Codex Desktop 앱은 **Codex 에이전트 전용** UI입니다. 처음 실행하면 다음과 같은 주요 영역이 보입니다.

- **Workspace(작업 폴더) 선택:** 에이전트가 읽고 쓸 수 있는 범위를 이 단계에서 결정합니다. 첫 폴더를 열 때 폴더 권한 허용 대화상자가 뜹니다.
- **Task / Agent 탭:** 자연어로 작업을 지시하면 에이전트가 계획 → 파일 변경 → diff 리뷰 → 커밋 단계로 진행합니다.
- **Sandbox 설정:** 쉘 명령 실행 허용 범위, 네트워크 접근 허용 여부를 토글할 수 있습니다. 초기값은 **읽기 전용**에 가까우므로 쓰기 작업을 시키려면 승인이 필요합니다.
- **Diff 리뷰 창:** 에이전트가 변경하려는 내용을 커밋 전에 하나씩 수락/거절할 수 있습니다 — 본 교재가 강조하는 "사람 승인 게이트"의 UI 버전입니다.

#### Windows · Linux — 브라우저 Codex

웹 UI도 Desktop 앱과 기능적으로 대응되는 영역을 갖고 있습니다. 명칭만 조금 다릅니다.

- **Environments(환경) / Repository 연결:** Workspace에 해당. GitHub 저장소를 연결하면 그 저장소 범위 안에서만 에이전트가 작업합니다.
- **Tasks 목록:** 에이전트가 받은 작업을 카드 형태로 큐잉합니다. 여러 작업을 병렬로 띄울 수 있습니다.
- **Sandbox 정책:** 환경 설정에서 네트워크·쉘 명령 허용 여부를 조정합니다. 기본값은 역시 보수적입니다.
- **PR 만들기 버튼:** 변경 내용을 GitHub PR로 자동 생성합니다 — 로컬 diff 리뷰 대신 PR 리뷰가 승인 게이트 역할을 합니다.

> 두 UI의 공통점은 명확합니다 — **"에이전트에게 맡기기 → 사람이 승인 → 코드 반영"** 3단계 구조. 이 구조가 harness 엔지니어링의 핵심 패턴이고, 뒷 단원들에서 CLI·hooks·MCP로 같은 패턴을 반복해 만납니다.

### 0-3. GUI + CLI 조합 (권장)

Codex Desktop 앱·브라우저 Codex(chatgpt.com/codex)·Codex CLI는 **모두 같은 ChatGPT 계정**을 공유합니다. 그래서 어느 쪽이든 한 번 로그인해 두면 CLI에서 별도 로그인 없이 바로 쓸 수 있는 경우가 많습니다. 학습자 대부분에게 가장 편한 순서는 다음과 같습니다.

- **macOS:** Codex Desktop 앱 설치·로그인 → CLI 설치(방식 A).
- **Windows·Linux:** 브라우저 Codex(chatgpt.com/codex)에 로그인 → CLI 설치(방식 A).

공통으로, 터미널에서 `codex`를 실행하면 `codex login` 없이 바로 프롬프트가 뜨는 경우가 많고, 그렇지 않으면 `codex login` 한 번만 돌리면 끝입니다.

> **자주 하는 혼동:** "앱에서는 로그인이 되는데 CLI가 왜 또 로그인을 요구하지?" — 앱과 CLI가 인증 토큰을 저장하는 위치가 OS에 따라 분리돼 있어서 그렇습니다. 이 경우 `codex login`을 한 번 돌려 주면 `~/.codex/auth.json`이 새로 생성되며 이후 실행부터는 자동 인증됩니다.

> **한계 안내.** 방식 0 단독으로는 이후 단원에서 다루는 `~/.codex/config.toml` 수정, `AGENTS.md` 파일 연동, MCP 서버 등록, `codex exec`로 CI 붙이기 같은 **harness 엔지니어링 실습이 제한**됩니다. 6단원 이후부터는 CLI 설치가 필수입니다.

### 0-4. (보너스 1) 다른 에이전트에게 Codex CLI 설치를 맡기기

"에이전트가 자기 다음 단계 도구를 설치해 주는" 실습은 플랫폼별로 진입점이 다릅니다.

- **macOS (Codex Desktop 앱 이용):** 앱의 Task/Agent 창에 아래 Mac용 프롬프트를 붙여 넣습니다.
- **Windows·Linux (Codex Desktop 앱 부재):** 이 실습은 **04단원에서 설치한 Claude Code CLI**에 맡기는 편이 가장 자연스럽습니다(아래 0-5절). 브라우저 Codex는 OpenAI 클라우드 샌드박스에서 돌기 때문에 내 로컬에 `codex`를 설치할 수 없습니다.

**Mac — Codex Desktop 앱 안에서:**

```text
내 Mac에 OpenAI Codex CLI를 설치해 줘. 설치 경로는 다음 세 가지 중 하나로,
내 환경에 맞는 것을 네가 판단해서 골라:
  - Homebrew가 있으면: `brew install codex`
  - Node.js v22 이상이 있으면: `npm install -g @openai/codex`
  - 둘 다 없으면: 둘 중 하나를 먼저 설치해 달라고 나에게 알려
설치가 끝나면 `codex --version`으로 확인하고,
위험해 보이는 명령이 있으면 실행 전에 반드시 나에게 먼저 알려 줘.
```

권한 팝업이 뜨면 스크립트 내용을 **눈으로 확인**한 뒤 "허용". 설치가 끝나면 터미널을 새로 열어 `codex --version`을 다시 확인하세요.

> **Windows·Linux 학습자에게:** Codex Desktop 앱이 없으므로 이 경로는 사용할 수 없습니다. 대신 아래 0-5절의 "Claude Code로 Codex 설치하기"로 진행하세요 — 본질적으로 같은 실습이며, 오히려 **다른 공급사의 에이전트에게 설치를 맡긴다**는 점에서 멀티 에이전트 오케스트레이션의 의미가 더 살아납니다.

### 0-5. (보너스 2) Claude Code로 Codex 설치하기 — 멀티 에이전트 첫 실습

이미 04단원에서 Claude Code CLI를 설치했다면, **Claude Code에게 Codex 설치를 맡기는 실습**이 가능합니다. 이게 이 과정이 다루는 "여러 에이전트를 역할별로 나눠 쓰기"의 가장 단순한 첫 사례이자, **Windows·Linux 학습자가 0-4를 대신해 쓰는 정식 경로**이기도 합니다.

터미널에서 작업 폴더로 이동한 뒤 `claude`를 실행하고, 프롬프트에 아래를 붙여 넣으세요.

```text
이 컴퓨터에 OpenAI Codex CLI를 설치해 줘. 환경 감지 기준은 다음과 같아:
- macOS + Homebrew: `brew install codex`
- macOS + Node 22+: `npm install -g @openai/codex`
- Windows PowerShell + Node 22+: `npm install -g @openai/codex`
  · 실행 정책이 막으면 `Set-ExecutionPolicy -Scope Process Bypass`를 먼저 적용
- Linux + Node 22+: `npm install -g @openai/codex`
설치 후 `codex --version`으로 검증하고, 그 출력까지 나에게 보여 줘.
쉘 명령은 실행 전에 어떤 의도로 쓰는지 한 줄 설명을 붙여 줘.
위험해 보이는 명령이 있으면 실행 전에 나에게 먼저 알려 줘.
```

> **교육적 의미.** Claude Code가 Codex 설치를 "진단 → 실행 → 검증" 3단계로 처리하는 과정을 지켜보면, 본 교재가 강조하는 **작업 정의 / 검증 계약 / 품질 게이트 / 에스컬레이션**의 4요소가 한 화면에서 눈에 들어옵니다. 또 "다른 공급사의 에이전트에게 경쟁사 CLI를 설치시킨다"는 구도 자체가, 이 과정 전체가 말하는 **도구-불가지적(tool-agnostic) 오케스트레이션** 철학의 축소판입니다.

---

## 1. OS: Mac

### 1-1. 터미널 열기

1. `Command (⌘) + Space` → `terminal` 입력 → Enter.
2. 아래 모든 명령은 이 창에 복사-붙여넣기(`⌘ + V`) 후 Enter.

### 1-2. 방식 A: 네이티브 CLI 설치 (권장)

Codex CLI는 Mac에서 **세 가지 공식 경로**를 제공합니다. 하나만 고르세요.

#### ① Homebrew — 가장 추천

Homebrew가 이미 있다면 한 줄로 끝납니다.

```bash
brew install codex
```

Homebrew가 없다면 먼저 설치하세요.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

설치 후 안내되는 `eval` 줄(예: `eval "$(/opt/homebrew/bin/brew shellenv)"`)을 그대로 `~/.zshrc`에 붙입니다. 이후:

```bash
brew install codex
codex --version
```

#### ② npm 전역 설치 — Node.js가 이미 있다면

먼저 Node.js 버전을 확인합니다.

```bash
node --version
```

`v22.x.x` 이상이면 바로 진행합니다. 아니라면 [04단원 1-3절](04_cc_install.md#1-3-방식-b-npm-전역-설치-nodejs가-이미-있는-경우)의 "Node.js 설치 — 선택지 3가지"에 따라 LTS를 먼저 설치하세요.

```bash
npm install -g @openai/codex
codex --version
```

`EACCES` 권한 오류가 나면 `sudo`를 **붙이지 말고**, 아래 문제 해결 절의 "npm 전역 권한" 항목을 보세요.

#### ③ 공식 바이너리 직접 설치 — Homebrew·Node 둘 다 싫을 때

1. 브라우저에서 [https://github.com/openai/codex/releases/latest](https://github.com/openai/codex/releases/latest) 접속.
2. Mac 아키텍처에 맞는 바이너리를 내려받습니다.
   - Apple Silicon(M1/M2/M3/M4): `codex-aarch64-apple-darwin.tar.gz`
   - Intel Mac: `codex-x86_64-apple-darwin.tar.gz`
3. 터미널에서 다운로드 폴더로 이동해 압축 해제 후 `/usr/local/bin`으로 이동.

```bash
cd ~/Downloads
tar -xzf codex-*-apple-darwin.tar.gz
sudo mv codex /usr/local/bin/codex
sudo chmod +x /usr/local/bin/codex
codex --version
```

macOS Gatekeeper가 "확인되지 않은 개발자" 경고를 띄우면 아래 한 줄로 격리 속성을 제거합니다.

```bash
xattr -d com.apple.quarantine /usr/local/bin/codex
```

### 1-3. 로그인 및 첫 실행

원하는 프로젝트 폴더로 이동해 `codex`를 실행합니다.

```bash
cd ~/Desktop
mkdir codex-test
cd codex-test
codex
```

처음 실행하면 **브라우저가 열리며 ChatGPT 로그인 화면**이 뜹니다. Plus/Pro/Business/Enterprise 중 하나의 계정으로 로그인합니다. API 키로 쓰고 싶다면 로그인 대신 환경변수를 쓸 수도 있습니다.

```bash
export OPENAI_API_KEY="sk-..."   # 임시로만 쓸 때
```

영구로 저장하려면 `~/.zshrc`에 위 줄을 추가하세요.

로그인이 끝나면 Codex TUI가 열립니다. 시험 삼아 아래를 입력.

```text
지금 폴더에 뭐가 있는지 알려 줘.
```

종료는 `/exit` 또는 `Ctrl + C`를 두 번.

### 1-4. 비대화형(스크립트) 실행 확인

Claude Code에 `claude -p`가 있다면 Codex에는 `codex exec`가 있습니다. CI/CD에서 쓰게 될 기본 형태를 미리 확인해 보세요.

```bash
codex exec "README.md 가 있는지 확인하고 없으면 한 줄짜리로 만들어 줘"
```

### 1-5. 환경 점검

```bash
codex --version
codex --help
ls ~/.codex
```

`~/.codex/` 아래에 `config.toml`, `auth.json`, `history.jsonl` 등이 생성돼 있으면 설치·인증이 정상입니다.

---

## 2. OS: Windows

### 2-1. 사전 준비: PowerShell 관리자 권한으로 열기

1. `Windows` 키 → `powershell` 입력.
2. "Windows PowerShell" 우클릭 → **관리자 권한으로 실행**.
3. UAC 팝업에서 **예**.

### 2-2. 방식 A: 네이티브 CLI 설치 (권장) — 두 경로

Windows에는 Codex 공식 Homebrew가 없으므로, 아래 둘 중 하나를 고릅니다.

#### ① npm 전역 설치 — 가장 일반적

먼저 Node.js가 있는지 확인.

```powershell
node --version
```

`v22.x.x` 이상이 아니면 아래 셋 중 하나로 Node.js LTS를 설치합니다(자세한 설명은 [04단원 2-4절](04_cc_install.md#node-js-설치--선택지-3가지-windows-공식-권장)).

```powershell
# 공식 .msi: https://nodejs.org/en/download 에서 Windows x64 LTS 내려받아 실행
# 또는 winget:
winget install OpenJS.NodeJS.LTS
# 또는 fnm (버전 매니저):
winget install Schniz.fnm
```

Node.js가 준비되면:

```powershell
npm install -g @openai/codex
codex --version
```

#### ② WSL(Ubuntu) 위에서 설치 — 이후 실습 친화적

6단원의 터미널·Git 실습과 자연스럽게 이어집니다. PowerShell(관리자)에서:

```powershell
wsl --install -d Ubuntu
```

재부팅 후 Ubuntu 터미널을 열고(사용자명·비밀번호 지정), Linux 쪽에서 Codex를 설치합니다.

```bash
# Node.js v22 LTS 설치 (NodeSource 공식 저장소)
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs

# Codex CLI 설치
npm install -g @openai/codex
codex --version
```

> **WSL + Node.js 조합에서 주의.** `sudo`로 npm 전역 설치를 하게 되는데, 가능하면 npm prefix를 사용자 홈으로 돌려두고 `sudo`를 피하는 게 장기적으로 안전합니다(문제 해결 절 참고).

### 2-3. 방식 B: 공식 바이너리 직접 설치 — Node·WSL 없이

1. [https://github.com/openai/codex/releases/latest](https://github.com/openai/codex/releases/latest) 접속.
2. Windows x64용 바이너리(`codex-x86_64-pc-windows-msvc.zip` 또는 `.exe`)를 내려받습니다.
3. 압축을 풀고 `codex.exe`를 원하는 위치에 둔 뒤 그 폴더를 PATH에 추가.

PowerShell(관리자)에서:

```powershell
# 예: C:\Tools\codex 폴더에 codex.exe를 둔 경우
$env:Path += ";C:\Tools\codex"
[Environment]::SetEnvironmentVariable("Path", $env:Path, [EnvironmentVariableTarget]::User)
codex --version
```

### 2-4. 로그인 및 첫 실행

PowerShell:

```powershell
cd $HOME\Desktop
mkdir codex-test
cd codex-test
codex
```

WSL(Ubuntu):

```bash
cd ~
mkdir codex-test
cd codex-test
codex
```

브라우저로 ChatGPT 로그인 화면이 열립니다. API 키 방식으로 쓰고 싶다면:

```powershell
# 임시 세션에서만
$env:OPENAI_API_KEY = "sk-..."

# 영구 저장
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-...", "User")
```

### 2-5. 비대화형 실행 및 환경 점검

```powershell
codex exec "README.md 가 있는지 확인하고 없으면 한 줄짜리로 만들어 줘"
codex --version
dir $HOME\.codex
```

---

## 3. 공통: 설치 확인 체크리스트

- [ ] `codex --version` 실행 시 버전 번호가 출력된다
- [ ] `codex --help` 실행 시 도움말이 정상 표시된다
- [ ] 임의의 폴더에서 `codex`를 실행하면 로그인 또는 TUI가 뜬다
- [ ] `codex exec "echo hi"` 같은 간단한 비대화형 명령이 동작한다
- [ ] 홈 디렉터리에 `~/.codex/` 폴더가 생성되었다

---

## 4. 문제 해결 (Troubleshooting)

### "command not found: codex" (Mac / WSL)

설치는 됐지만 현재 셸 세션이 PATH 변경을 반영하지 못한 상태입니다. 터미널을 **완전히 닫았다 다시 여세요**. 그래도 같다면:

```bash
# Homebrew로 설치한 경우: Apple Silicon은 /opt/homebrew/bin, Intel은 /usr/local/bin
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# npm 사용자 prefix로 설치한 경우
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### "EACCES: permission denied" (npm 방식)

`sudo npm install -g`로 우회하지 마세요. 대신 전역 prefix를 사용자 홈으로 옮깁니다.

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
npm install -g @openai/codex
```

### "unable to verify the first certificate" / 사내 프록시 뒤에서 설치 실패

사내 네트워크에서 TLS 인터셉트가 걸려 있을 가능성이 높습니다. IT팀에 아래 도메인 허용을 요청하세요.

- `registry.npmjs.org` (npm 방식)
- `formulae.brew.sh`, `ghcr.io` (Homebrew)
- `github.com`, `objects.githubusercontent.com` (바이너리 다운로드)
- `api.openai.com`, `auth.openai.com`, `chatgpt.com` (로그인 · 실행)

### 로그인 브라우저가 열리지 않을 때

터미널에 표시되는 **URL과 인증 코드**를 직접 브라우저에 복사해 붙여 넣으면 됩니다. SSH로 원격 서버에 접속한 상태일 때도 동일합니다.

### "Unsupported Node.js version" 같은 오류

Codex CLI는 Node.js **v22 이상**을 요구합니다. `node --version`이 v20 이하라면 LTS v22로 업그레이드하세요.

### macOS "Apple이 확인되지 않은 개발자" 경고

공식 바이너리를 직접 내려받아 쓴 경우 발생합니다. 격리 속성만 제거하면 됩니다.

```bash
xattr -d com.apple.quarantine /usr/local/bin/codex
```

### Codex 앱에서는 로그인되는데 CLI가 계속 로그인을 요구한다

앱과 CLI의 인증 저장소가 분리돼 있을 수 있습니다. CLI에서 명시적으로 로그인하세요.

```bash
codex login
```

성공하면 `~/.codex/auth.json`이 생성되고 이후 실행부터는 자동 인증됩니다.

---

## 5. Claude Code와 Codex를 같은 컴퓨터에 공존시키기

이 과정은 두 에이전트를 **같은 폴더에서 번갈아 쓰는 실습**이 핵심입니다. 공존 체크리스트는 다음과 같습니다.

- [ ] `claude --version`과 `codex --version`이 둘 다 동작한다
- [ ] 홈 디렉터리에 `~/.claude/`와 `~/.codex/` 폴더가 **분리되어** 존재한다
- [ ] 같은 프로젝트 폴더에 `CLAUDE.md`(Claude Code용)와 `AGENTS.md`(Codex용)를 **따로** 둘 수 있다(다음 단원에서 다룹니다)
- [ ] 쉘 프로필(`.zshrc`/`$PROFILE`)에 `OPENAI_API_KEY`와 `ANTHROPIC_API_KEY`를 섞어 쓸 경우, 두 값이 **서로 덮어쓰지 않는지** 확인

> 두 도구는 인증·설정·실행 경로가 전부 분리돼 있어 **충돌하지 않습니다.** 다만 `/usr/local/bin`처럼 PATH 우선순위가 같은 곳에 서로 다른 방식(Homebrew vs 바이너리)으로 중복 설치하면 버전 혼선이 날 수 있으니, **설치 경로를 하나로 통일**하세요.

---

## 6. 다음으로

설치가 끝났으면 [06. 터미널과 Git](06_terminal_and_git.md)으로 넘어가세요. 거기서부터는 `claude`와 `codex`를 **같은 Git 저장소 위에서 번갈아 사용**하면서, harness 엔지니어링의 기본 루틴(`clone → branch → commit → push`)을 두 에이전트 관점에서 동시에 익힙니다.

> **한 줄 요약:** Mac은 `brew install codex`, Windows는 `npm install -g @openai/codex` 한 줄이면 끝. 앱 경로로 시작해도, 결국 본 실습은 CLI로 진행됩니다.
