# 04. Claude Code 설치 가이드

> 이 문서는 **터미널을 처음 여는 분**도 복사-붙여넣기만으로 따라올 수 있도록 작성했습니다. 명령어는 한 줄씩 그대로 복사해서 터미널에 붙여 넣고 Enter를 누르면 됩니다. 실행 결과가 예상과 다르면 **절대 다음 단계로 넘어가지 말고** 문서 맨 아래 "문제 해결" 절을 먼저 확인하세요.

---

## 0. 설치 전에 알아둘 것

Claude Code는 터미널(명령어 창)에서 동작하는 **AI 코딩 에이전트 CLI**입니다. 즉, 브라우저에서 쓰는 Claude.ai와 달리 **내 컴퓨터의 파일과 Git 저장소를 직접 읽고 수정**할 수 있습니다. 그래서 설치 과정에서 "터미널"이라는 도구를 잠깐 만나야 합니다.

설치 방식은 세 가지입니다.

| 방식 | 장점 | 추천 대상 |
|------|------|-----------|
| **0. Claude Desktop 앱 (GUI)** | 설치 파일 더블 클릭으로 끝. 터미널 없이 맛보기 가능 | 터미널이 처음이라 부담스러운 분 |
| **A. 네이티브 CLI 설치 (권장)** | Node.js·npm을 따로 설치하지 않아도 됨. 자동 업데이트 내장 | 이 교재의 본 실습을 하실 분 |
| **B. npm 전역 설치** | 이미 Node.js를 쓰고 있다면 친숙함 | 프런트엔드 개발 경험자 |

**세 방식을 동시에 설치하지 마세요.** 하나만 고르면 됩니다. 단, 방식 0과 A는 **병행 가능**합니다 — 앱으로 로그인해 두면 CLI가 그 인증 정보를 그대로 재사용하기 때문에 학습 초기에 편합니다. 이 교재의 본 실습(Git·터미널·hooks·MCP)은 **CLI가 주 무대**이므로, 방식 0만으로는 4단원 이후 일부 기능을 그대로 따라 할 수 없습니다.

---

## 방식 0. Claude Desktop 앱으로 빠르게 시작하기 (공통)

터미널이 처음이라 부담스럽다면 **Claude Desktop 앱**부터 설치하는 게 가장 쉽습니다. 최근 Desktop 앱은 Claude Code 실행 환경을 내장하고 있어, 앱 안의 "Claude Code" 탭(또는 `Ctrl/⌘ + K`로 열리는 패널)에서 에이전트를 바로 띄울 수 있습니다.

### 0-1. 앱 다운로드

1. 브라우저에서 [https://claude.ai/download](https://claude.ai/download) 접속.
2. OS에 맞는 설치 파일을 받아 실행.
   - Mac: `Claude.dmg` → 드래그로 Applications 폴더에 복사.
   - Windows: `Claude-Setup.exe` → "다음 → 설치".
3. 앱 실행 후 Anthropic 계정(Claude Pro/Max)으로 로그인.

### 0-2. 앱 안에서 Claude Code 열기

1. 앱 왼쪽 사이드바에서 **Claude Code** 항목을 선택하거나, 상단 "+ New" → "Code" 선택.
2. 작업할 폴더를 선택하면(Mac은 폴더 권한 허용 대화상자가 뜹니다), 그 폴더 범위 안에서 Claude가 파일을 읽고 수정합니다.
3. 채팅창에 지시를 입력하면 끝.

### 0-3. 앱 + CLI 조합 (권장)

앱에서 한 번만 로그인하면 **같은 계정의 CLI도 재로그인이 필요 없습니다.** 그래서 학습자 대부분에게 가장 편한 순서는 이렇습니다.

1. 방식 0으로 Desktop 앱 설치 & 로그인.
2. 이어서 방식 A로 CLI 설치.
3. 터미널에서 `claude`를 실행하면 로그인 창 없이 바로 `>` 프롬프트가 뜹니다.

> **한계 안내.** 방식 0 단독으로는 이후 단원의 `~/.claude/settings.json` 편집, hooks, 서브에이전트 병렬 실행, MCP 서버 등록 같은 **harness 엔지니어링 실습이 제한**됩니다. 6단원 이후부터는 CLI 설치가 필수입니다. 이 점을 염두에 두고, 5분 맛보기는 앱으로, 본 실습은 CLI로 진행하세요.

### 0-4. (보너스) 앱에게 CLI 설치를 맡기기 — harness 엔지니어링 첫 실습

방식 0으로 Desktop 앱을 깐 뒤, **CLI 설치조차 에이전트에게 맡길 수 있습니다.** 앱 안의 Claude Code는 이미 쉘 실행 권한을 갖고 있어서, 스스로 설치 스크립트를 돌릴 수 있기 때문입니다. 이 과정 자체가 본 교재가 다루는 "AI에게 검증 가능한 작업을 위임하고, 위험한 순간에만 사람이 개입한다"는 원칙의 첫 실습 사례이기도 합니다.

#### 시도하는 방법

1. Desktop 앱에서 작업 폴더를 하나 열고, Claude Code 탭을 활성화.
2. 채팅창에 아래를 그대로 붙여 넣고 Enter.

**Mac인 경우:**

```text
내 Mac에 Claude Code CLI 네이티브 버전을 설치해 줘.
공식 스크립트는 `curl -fsSL https://claude.ai/install.sh | bash` 이야.
설치가 끝나면 `claude --version` 으로 설치 확인까지 해 줘.
중간에 위험한 명령이 있으면 실행 전에 나한테 먼저 알려 줘.
```

**Windows인 경우 (PowerShell이 설치 대상):**

```text
내 Windows에 Claude Code CLI 네이티브 버전을 PowerShell 기준으로 설치해 줘.
공식 스크립트는 `irm https://claude.ai/install.ps1 | iex` 이야.
실행 정책이 막는 경우엔 `Set-ExecutionPolicy -Scope Process Bypass`를 먼저 적용해.
설치 후 `claude --version`으로 확인까지 해 주고, 위험한 명령은 실행 전에 알려 줘.
```

3. 에이전트가 Bash(또는 PowerShell) 도구를 호출하려 할 때 앱이 **권한 팝업**을 띄웁니다. 내용이 위 스크립트와 일치하는지 **반드시 눈으로 확인**하고 "허용"을 누르세요. 여기가 이번 실습의 가장 중요한 지점입니다.
4. 설치가 끝나면 터미널(Mac: Terminal, Windows: PowerShell)을 **새로** 열고 `claude --version`을 직접 한 번 더 확인합니다. 앱 안에서 확인되더라도, 시스템 전역 PATH가 내 터미널에 제대로 붙었는지는 별개이기 때문입니다.

#### 이 방식의 의미 (교재 맥락과 연결)

- 이건 단순한 "편의 기능"이 아니라 **harness 엔지니어링의 축소판**입니다.
  - 작업 정의: "무엇을 설치할지, 공식 명령은 무엇인지" 사람이 명시
  - 검증 계약: "`claude --version`으로 확인" — AI가 성공을 스스로 증명해야 함
  - 품질 게이트: 권한 팝업 = 사람 승인 게이트
  - 에스컬레이션: "위험한 명령이 있으면 먼저 알려 줘" — 자율성의 상한선 지정
- 반대로, 아래 경우엔 이 방식을 쓰지 마세요.
  - 사내 보안 정책이 스크립트 기반 설치를 금지하는 경우 (IT팀 승인 없이 진행하면 감사 이슈)
  - 프록시·서명 검증이 걸려 있어 스크립트 실행이 중간에 실패할 가능성이 높은 경우
  - CI/CD 서버처럼 여러 사람이 공유하는 환경 (전역 설치는 공용 환경을 오염시킵니다)

> **검증 습관.** 에이전트가 "설치 완료"라고 말해도, 항상 **새 터미널**에서 `claude --version`과 `claude doctor`를 직접 실행해 확인하세요. AI의 "완료"는 명령이 돌아간 시점일 뿐이고, 내 셸 환경에 반영됐는지는 별개입니다. 이 습관 하나가 이 과정 전체에서 가장 자주 쓰이는 검증 루틴이 됩니다.

---

## 1. OS: Mac

### 1-1. 터미널 열기

1. `Command (⌘) + Space`를 눌러 Spotlight를 엽니다.
2. `terminal`이라고 입력하고 Enter.
3. 검은색(또는 흰색) 창이 하나 뜹니다. 이것이 **터미널**입니다.

> 아래부터 "터미널에 입력"이라고 하면 이 창에 명령어를 복사-붙여넣기(`⌘ + V`) 한 뒤 Enter를 누른다는 뜻입니다.

### 1-2. 방식 A: 네이티브 설치 (권장)

아래 한 줄을 **통째로** 복사해 터미널에 붙여 넣고 Enter.

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

설치가 끝나면 아래처럼 "Installed successfully" 같은 메시지가 나타납니다. 설치 스크립트는 `~/.local/bin` 같은 위치에 `claude` 실행 파일을 놓고, 자동으로 PATH(명령어 검색 경로)에 추가합니다.

설치가 끝났으면 **터미널을 완전히 닫았다가 다시 여세요**. PATH 변경이 반영되려면 새 창이 필요합니다.

새 터미널에서 아래 명령으로 설치를 확인합니다.

```bash
claude --version
```

버전 번호(예: `2.x.x (Claude Code)`)가 출력되면 성공입니다.

### 1-3. 방식 B: npm 전역 설치 (Node.js가 이미 있는 경우)

먼저 Node.js가 설치돼 있는지 확인합니다.

```bash
node --version
```

- `v20.x.x` 이상이 출력되면 바로 "Claude Code 설치" 단계로 갑니다.
- `command not found`가 뜨거나 v18 이하가 뜨면, 아래 세 가지 중 **하나만** 골라 Node.js를 설치하세요.

#### Node.js 설치 — 선택지 3가지

Node.js 공식 사이트([https://nodejs.org/en/download](https://nodejs.org/en/download))가 공식 권장하는 세 경로입니다. 취향대로 고르면 됩니다.

##### ① 공식 설치 파일(.pkg) — 가장 쉬움

1. 브라우저에서 [https://nodejs.org/en/download](https://nodejs.org/en/download) 접속.
2. 화면 상단에서 **LTS** 버전(짝수 번호, 예: 22.x)을 선택하고, OS는 **macOS**, 방법은 **Prebuilt Installer**를 선택.
3. 내려받은 `.pkg` 파일을 더블 클릭해 "다음 → 다음 → 설치" 순으로 진행.
4. 설치가 끝나면 **터미널을 새로 열어** 아래로 확인.

```bash
node --version
npm --version
```

##### ② 공식 버전 매니저(`nvm`) — 여러 Node 버전을 쓰게 될 분에게 권장

nvm은 Node.js 공식 문서가 "프로젝트별 다른 버전을 써야 할 때 권장"하는 버전 매니저입니다.

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
```

설치 후 터미널을 새로 열고:

```bash
nvm install --lts
nvm use --lts
node --version
```

##### ③ Homebrew — 이미 Homebrew를 쓰고 있다면

Homebrew가 없다면 먼저 설치하세요.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

설치가 끝나면 터미널이 안내하는 `eval` 줄(예: `eval "$(/opt/homebrew/bin/brew shellenv)"`)을 복사해 `.zshrc`에 추가하라고 알려 줍니다. 그 안내를 그대로 따라 하세요.

이어서 Node.js LTS 설치:

```bash
brew install node@22
```

확인:

```bash
node --version
npm --version
```

> **세 방법을 동시에 쓰지 마세요.** 설치 경로가 섞이면 `command not found`·버전 충돌의 원인이 됩니다. 이미 다른 방법으로 설치돼 있다면 그걸 그대로 쓰세요.

#### Claude Code 설치

```bash
npm install -g @anthropic-ai/claude-code
```

`EACCES` 같은 권한 오류가 나면 앞에 `sudo`를 붙이지 **말고**, 아래 문제 해결 절의 "npm 전역 권한" 항목을 보세요. `sudo npm`은 나중에 꼬이는 원인이 됩니다.

설치 확인:

```bash
claude --version
```

### 1-4. 로그인 및 첫 실행

원하는 프로젝트 폴더로 이동한 뒤 `claude`를 실행합니다. 예시:

```bash
cd ~/Desktop
mkdir claude-test
cd claude-test
claude
```

처음 실행하면 **브라우저가 열리며 Anthropic 로그인 화면**이 뜹니다. Claude Pro/Max 계정 또는 Anthropic Console의 API 키 둘 중 하나로 로그인하면 됩니다(교재는 Claude Pro/Max 구독을 가정합니다).

로그인이 끝나면 터미널에 `>` 프롬프트가 나타납니다. 시험 삼아 아래를 입력해 보세요.

```text
안녕? 지금 작업 중인 폴더에 어떤 파일이 있는지 알려줘.
```

Claude가 `ls` 같은 도구를 호출해 폴더 상태를 설명해 주면 설치 성공입니다. 종료하려면 `/exit` 또는 `Ctrl + C`를 두 번 누릅니다.

### 1-5. 환경 점검 (중요)

설치 직후 아래 명령으로 환경을 점검하세요. MCP 서버, 터미널 렌더링, 자동 업데이트 경로를 한 번에 검사해 줍니다.

```bash
claude doctor
```

모두 녹색(또는 ✓)이면 다음 단원으로 넘어가도 좋습니다.

---

## 2. OS: Windows

Windows는 두 가지 경로가 있습니다. 본 교재는 **네이티브 PowerShell 설치**를 기본으로 하되, 이후 Git·터미널 실습을 원활히 하기 위해 **WSL(Ubuntu on Windows)** 경로도 함께 제공합니다. 한 번에 하나만 고르세요.

### 2-1. 사전 준비: PowerShell 관리자 권한으로 열기

1. 키보드 `Windows` 키를 누릅니다.
2. `powershell`이라고 입력합니다.
3. "Windows PowerShell"에 마우스 우클릭 → **관리자 권한으로 실행**.
4. "이 앱이 디바이스를 변경하도록 허용하시겠어요?"가 뜨면 **예**.

> "관리자 권한"을 요구하는 이유는 설치 스크립트가 PATH 환경변수를 사용자 계정에 등록하기 때문입니다. 일반 PowerShell 창에서도 되긴 하지만, 초보자는 관리자 창으로 시작하는 편이 실수가 적습니다.

### 2-2. 방식 A: 네이티브 설치 (권장)

실행 정책 때문에 스크립트가 막히는 일을 방지하기 위해, 먼저 **이번 PowerShell 세션에 한해** 스크립트 실행을 허용합니다.

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
```

이어서 설치 스크립트를 실행합니다.

```powershell
irm https://claude.ai/install.ps1 | iex
```

> `irm`은 `Invoke-RestMethod`의 줄임말로 URL에서 파일을 받아오는 명령이고, `iex`는 `Invoke-Expression`으로 받은 내용을 실행합니다. 즉 "설치 스크립트를 다운로드하자마자 바로 실행한다"는 뜻입니다.

설치가 끝나면 **PowerShell 창을 완전히 닫고 새로 여세요.** PATH 변경은 새 창부터 반영됩니다.

새 창에서 확인합니다.

```powershell
claude --version
```

버전 번호가 출력되면 성공입니다.

### 2-3. 방식 B: WSL(Ubuntu) 위에서 설치 — 이후 실습 친화적

6단원의 터미널·Git 실습과 이어서 작업할 분께 권장하는 방식입니다. Windows에서 리눅스 환경을 얹어 그 위에서 Claude Code를 돌립니다.

#### WSL + Ubuntu 설치

PowerShell(관리자 권한)에서:

```powershell
wsl --install -d Ubuntu
```

설치가 끝나면 PC를 **재부팅**하세요. 재부팅 뒤 자동으로 Ubuntu 터미널이 뜨면서 사용자 이름과 비밀번호를 물어봅니다. 아무거나 편한 값으로 지정합니다(비밀번호 입력 시 화면에 점조차 찍히지 않지만 정상입니다).

> 재부팅 뒤 자동으로 창이 뜨지 않으면, 시작 메뉴에서 `Ubuntu`를 검색해 직접 실행하세요.

#### Ubuntu 터미널에서 Claude Code 설치

아래부터는 **Ubuntu 터미널**에 붙여 넣습니다. (PowerShell이 아닙니다.)

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

새 Ubuntu 터미널을 열고 확인:

```bash
claude --version
```

### 2-4. 방식 C: npm 전역 설치 (Node.js 경험자용)

npm을 쓰려면 먼저 Node.js가 있어야 합니다. PowerShell에서 확인:

```powershell
node --version
```

`v20.x.x` 이상이면 바로 "Claude Code 설치" 단계로. 아니라면 아래 셋 중 **하나만** 고르세요.

#### Node.js 설치 — 선택지 3가지 (Windows 공식 권장)

Node.js 공식 사이트([https://nodejs.org/en/download](https://nodejs.org/en/download))가 Windows에 공식 권장하는 세 경로입니다.

##### ① 공식 설치 파일(.msi) — 가장 쉬움

1. 브라우저에서 [https://nodejs.org/en/download](https://nodejs.org/en/download) 접속.
2. **LTS** 버전 선택 → OS는 **Windows** → 방법은 **Prebuilt Installer** → 아키텍처는 **x64**(대부분의 PC) 또는 **arm64**(Snapdragon/Surface Pro X 등).
3. 내려받은 `node-v22.x.x-x64.msi` 파일을 더블 클릭.
4. 설치 화면에서 "Add to PATH"가 체크돼 있는지만 확인하고 "Next → Install".
5. 설치가 끝나면 **PowerShell 창을 새로 열어** 확인.

```powershell
node --version
npm --version
```

##### ② 공식 버전 매니저(`fnm`) — 여러 Node 버전을 쓰게 될 분에게 권장

Node.js 공식 문서가 Windows 전용 "Fast Node Manager"로 안내하는 방식입니다(예전의 nvm-windows보다 최신).

PowerShell(관리자)에서 `winget`으로 설치:

```powershell
winget install Schniz.fnm
```

PowerShell을 새로 연 뒤 환경을 활성화:

```powershell
fnm env --use-on-cd | Out-String | Invoke-Expression
```

이 한 줄을 매번 실행하기 싫다면 PowerShell 프로필에 추가하세요.

```powershell
Add-Content -Path $PROFILE -Value 'fnm env --use-on-cd | Out-String | Invoke-Expression'
```

LTS 설치:

```powershell
fnm install --lts
fnm use lts-latest
node --version
```

##### ③ `winget`으로 바로 설치 — 빠르게 끝내고 싶다면

Windows 10 21H1 이상에 기본 탑재된 공식 패키지 매니저 `winget`으로 한 줄 설치가 가능합니다.

```powershell
winget install OpenJS.NodeJS.LTS
```

설치 후 PowerShell을 새로 열고:

```powershell
node --version
npm --version
```

> **세 방법을 동시에 쓰지 마세요.** 특히 공식 `.msi`로 설치한 상태에서 `fnm`을 얹으면 PATH 우선순위가 꼬여 `node` 버전이 뒤섞입니다. 이미 하나로 설치돼 있다면 그걸 그대로 쓰세요.

#### Claude Code 설치

```powershell
npm install -g @anthropic-ai/claude-code
```

```powershell
claude --version
```

> Windows 네이티브 npm은 경로·권한 이슈가 잦습니다. 가능하면 방식 A(네이티브 설치) 또는 B(WSL)를 권장합니다.

### 2-5. 로그인 및 첫 실행

원하는 폴더로 이동해 `claude`를 실행합니다.

PowerShell에서:

```powershell
cd $HOME\Desktop
mkdir claude-test
cd claude-test
claude
```

Ubuntu(WSL)에서:

```bash
cd ~
mkdir claude-test
cd claude-test
claude
```

Mac과 동일하게 브라우저가 열리며 로그인 화면이 뜹니다. 로그인이 끝나면 `>` 프롬프트가 나타납니다.

### 2-6. 환경 점검

```powershell
claude doctor
```

(WSL에서는 `claude doctor`를 그대로 Ubuntu 터미널에 입력)

---

## 3. 공통: 설치 확인 체크리스트

모두 ✓가 떠야 다음 단원으로 넘어갑니다.

- [ ] `claude --version` 실행 시 버전 번호가 출력된다
- [ ] `claude doctor` 실행 시 오류 없이 통과한다
- [ ] 임의의 폴더에서 `claude`를 실행하면 로그인 또는 `>` 프롬프트가 뜬다
- [ ] `/exit` 명령으로 깔끔하게 종료된다

---

## 4. 문제 해결 (Troubleshooting)

### "command not found: claude" (Mac / WSL)

설치 스크립트가 PATH에 실행 파일 위치를 추가했지만, **현재 터미널 세션이 아직 반영되지 않았기 때문**입니다. 터미널을 **완전히 닫았다 다시 여세요**. 그래도 같다면:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

(bash 사용자는 `.zshrc`를 `.bashrc`로 바꾸세요.)

### "claude : 이 시스템에서 스크립트를 실행할 수 없으므로..." (Windows)

PowerShell 실행 정책에 막혔습니다. 관리자 PowerShell에서:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

`Y`를 눌러 수락합니다.

### "EACCES: permission denied" (Mac, npm 방식)

`sudo`로 우회하지 **마세요**. 대신 npm의 전역 경로를 사용자 홈으로 옮깁니다.

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
npm install -g @anthropic-ai/claude-code
```

### 로그인 브라우저가 열리지 않을 때

`claude`를 실행했을 때 화면에 표시되는 **URL과 인증 코드**를 직접 브라우저에 붙여 넣으면 됩니다. SSH로 원격 서버에 접속한 경우에도 동일하게 동작합니다.

### `node --version`은 잘 뜨는데 `npm install -g`에서 버전 경고가 나올 때

Claude Code는 Node.js **v20 이상**을 요구합니다. `v18` 이하라면 위의 공식 설치 경로 중 하나로 LTS(v22 등)를 다시 설치하세요. 공식 `.pkg`/`.msi`로 재설치하면 이전 버전을 덮어씁니다.

### 사내 네트워크에서 설치가 막힐 때

프록시·방화벽 환경이라면 IT팀에 아래 도메인 허용 요청을 전달하세요.

- `claude.ai`
- `api.anthropic.com`
- `console.anthropic.com`
- `registry.npmjs.org` (npm 방식만)

---

## 5. 다음으로

설치가 끝났으면 바로 [05. Codex Install](05_cx_install.md)로 넘어가 Codex CLI도 함께 준비해 두세요. 이후 [06. 터미널과 Git](06_terminal_and_git.md) 단원에서 두 에이전트를 같은 실습 위에서 나란히 비교합니다.

> **한 줄 요약:** 터미널이 처음이면 [claude.ai/download](https://claude.ai/download)에서 Desktop 앱부터, 본 실습은 Mac `curl … install.sh | bash` / Windows `irm … install.ps1 | iex` 한 줄이면 끝. 앱과 CLI는 같은 계정으로 **같이 설치해도 됩니다**.
