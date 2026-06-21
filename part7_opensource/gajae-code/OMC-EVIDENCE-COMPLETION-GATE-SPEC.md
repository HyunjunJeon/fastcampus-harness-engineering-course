# 사양 - OMC 증거 기반 완료 게이트

- **상태:** 설계 고정됨(요구사항/인터뷰 단계 완료). 구현은 시작하지 않았습니다. ralplan 합의 계획이 작성 중이며 승인 대기 상태로 보관됩니다. 명시적 승인 없이는 실행하지 않습니다.
- **날짜:** 2026-06-21
- **출처:** 2라운드 소크라테스식 인터뷰(9개 결정 확인). 이 문서는 권위 있는 설계 계약입니다.
- **대상 시스템:** `oh-my-openagent`(OMC) - `part7_opensource/oh-my-openagent/`, 멀티 하네스(OpenCode + Codex/lazycodex 어댑터).
- **가져온 패턴:** Gajae-Code(gjc) - 증거 기반 완료 게이트(`ultragoal` Stop-hook `decision:block` + `team` `completion_evidence_no_verified_item` + 암호학적 영수증 신선도 만료). `part7_opensource/gajae-code/ORCHESTRATION-MODES-GJC-VS-OMC.md` Part 6 #2를 참고합니다(공유 설계 DNA: 증거 기반 완료).

> 주의: `part7_opensource/oh-my-openagent/` 아래 OMC 소스는 스냅샷이며 오래되었을 수 있습니다(`part7_opensource/AGENTS.md` 참고). 아래 모든 `file:line`/경로 참조는 구현 전에 현재 OMC 소스 기준으로 반드시 다시 검증해야 합니다.

---

## 1. 문제와 목표

OMC는 이미 증거를 의무화합니다("NO EVIDENCE FILE == NO QA == NO COMMIT == NO PUSH", `oh-my-openagent/AGENTS.md`). 하지만 현재 강제 방식은 **프롬프트/스킬 규율**입니다(AGENTS.md 의무 + `.omo/evidence/`에 기록하는 `opencode-qa`/`codex-qa` 스킬). 협조적이지 않거나 잊어버린 모델은 여전히 신선한 검증 없이 "done"을 선언할 수 있습니다.

**목표:** 증거 의무를 프롬프트 규율에서 **코드로 강제되는 완료 게이트**로 전환합니다. 연결된 컴포넌트를 건드린 세션은 현재 작업트리와 파일 해시가 일치하는 검증 항목이 ledger에 없으면 턴을 끝낼 수 없습니다.

**비목표:** QA 스킬 교체(QA 스킬은 계속 증거 생산자로 남음), gjc의 전체 암호학적 영수증 장치 구축, 연결되지 않은 작업(문서만 수정/읽기 전용) 게이팅, 병렬성/재개 기능.

---

## 2. 확인된 결정(인터뷰)

| # | 결정 지점 | 선택 | 근거 |
|---|---|---|---|
| D1 | 주입 지점 | **Stop/SubagentStop hook**(`start-work-continuation` 패턴 확장) -> `decision:block` | gjc와 1:1 대응. 차단 primitive가 이미 있으므로 새 infra 불필요 |
| D2 | 증거 계약 | **하이브리드** - JSON ledger가 `.omo/evidence/` 파일을 참조하고 `content_sha256`으로 봉인 | gjc receipt 결. 기존 evidence dir 재사용, 위조 방지 |
| D3 | 강제 방식 | **강한 차단 + 명시적 턴별 우회 플래그(사유 포함)** | gjc의 강도 + OMC의 실용성(hotfix 탈출구) |
| D4 | 범위 트리거 | **연결된 컴포넌트가 편집된 경우에만** | 기존 "hook/tool/...을 건드리면 QA" 의무를 반영. 모든 턴 차단 방지 |
| D5 | 배치 | **두 어댑터가 함께 사용하는 공유 Core package** | 진행 중인 package-layering refactor와 일치 |
| D6 | 완료 트리거 | **PostToolUse가 연결 컴포넌트 편집 시 세션 `dirty` 플래그 설정** -> Stop이 `dirty && no fresh evidence` 검사 | 범위 결정(D4)을 직접 구현. 결정적 동작 |
| D7 | 신선도 | **변경 파일 집합 + 파일별 `content_sha256`을 ledger에 봉인**. Stop 시 불일치 -> 증거 stale -> block | gjc staleness 결. 어제 evidence dir 재사용 차단 |
| D8 | Ledger 작성 주체 | **PostToolUse가 Bash/test exit code를 자동 캡처** -> agent가 위조할 수 없음 | gjc "비협조 모델도 우회할 수 없음" |
| D9 | 우회 + 감사 | **턴별 명시 사유 필수**, audit log에 추가, **Stop 후 자동 clear**(비영속, 매번 재진술 필요) | gjc "우회 시도는 기록됨" 결 |

---

## 3. 아키텍처 - 3개 조각

```
PostToolUse(edit) ─┐
                   ├─▶ evidence-collector ──▶ evidence-ledger.json ──▶ evidence-gate ──▶ ALLOW | {decision:block}
PostToolUse(Bash) ─┘   (dirty 표시 +           (세션 범위)             (Stop / SubagentStop)
                        exit_code 자동 캡처)
```

1. **evidence-collector**(PostToolUse): 연결된 경로에 대한 `write`/`edit`/`apply_patch`가 발생하면 `dirty=true`를 설정하고 경로를 기록합니다. `Bash`에서는 `{cmd, exit_code}`를 캡처합니다. `exit_code==0`이고 cmd가 검증 패턴과 일치하면 모든 dirty 연결 파일의 현재 `content_sha256`을 `bound_files`로 포함한 검증 항목을 추가합니다.
2. **evidence-gate**(Stop, SubagentStop): 결정 알고리즘(섹션 5)을 실행합니다. 조건이 충족되지 않으면 `{"decision":"block","reason":...}`를 방출합니다. 이는 `start-work-continuation`과 동급입니다.
3. **`evidence-gate-core`**(새 shared package): 하네스에 독립적인 로직입니다. ledger 읽기/쓰기, sha256, 연결 경로 matcher, 신선도 검사, 결정 함수, 우회 + 감사를 담당합니다. 두 어댑터가 이를 호출합니다.

---

## 4. 데이터 모델 - ledger

위치: `$PLUGIN_DATA/sessions/<id>/evidence-ledger.json`(`rules` 컴포넌트 세션 캐시 `$PLUGIN_DATA/sessions/<id>.json`와 같은 방식). 사람이 보는 artifact는 `.omo/evidence/<YYYYMMDD>-<slug>/` 아래에 남고, ledger가 이를 참조하며 해시로 고정합니다.

```jsonc
{
  "session_id": "string",
  "dirty": true,
  "connected_paths": ["packages/omo-opencode/src/hooks/lsp/index.ts"],
  "items": [
    {
      "kind": "test | build | qa-skill",
      "cmd": "bun run test:codex",
      "exit_code": 0,
      "captured_at": "ISO-8601",
      "artifact": ".omo/evidence/20260621-x/app-server-drive.json",
      "artifact_sha256": "...",
      "bound_files": [ { "path": "...", "sha256": "..." } ]   // 캡처 시점의 worktree hash(신선도 봉인)
    }
  ],
  "bypass": null   // 또는 { "reason": "string", "at": "ISO-8601" } - 한 턴에만 설정, Stop 시 자동 clear
}
```

---

## 5. 결정 알고리즘(Stop / SubagentStop)

```ts
const s = readLedger(sessionId);
if (!s.dirty) return ALLOW;                              // D4/D6: 연결 컴포넌트를 건드리지 않음
if (s.bypass?.reason) { audit.append(s.bypass); clearBypass(s); return ALLOW; }  // D9

const fresh = s.items.filter(it =>
  it.exit_code === 0 && hashesMatchWorktree(it.bound_files));   // D7 신선도

if (fresh.length === 0) {
  return {
    decision: "block",
    reason: "completion_evidence_no_fresh_verified_item: 연결된 컴포넌트가 편집되었지만 현재 작업트리 상태를 포괄하는 통과 검증이 없습니다. opencode-qa/codex-qa를 실행하거나 테스트를 다시 실행한 뒤 완료하세요."
  };
}
return ALLOW;
```

**신선도 불변식(D7):** test가 통과한 뒤 dirty 연결 파일이 하나라도 편집되면 해당 파일의 `content_sha256`이 item의 `bound_files`와 더 이상 일치하지 않습니다. 그러면 그 item은 `fresh`가 아니며 재검증이 강제됩니다. 이는 gjc의 `qualityGateHash` + `planGeneration` 신선도 만료를 OMC에 대응시킨 것입니다.

---

## 6. 범위 감지 - "연결된 컴포넌트"(D4)

기존 의무("hook, tool, agent, feature, config schema, MCP, CLI command, installer, prompt")와 일치하는 경로는 연결된 것으로 봅니다. 초기 glob 집합(계획에서 확정 예정):

- `packages/omo-opencode/**`
- `packages/omo-codex/**`
- `packages/*-core/**`, `packages/*-mcp/**`
- 모든 `**/hooks/**`, `**/tools/**`, `**/agents/**`, `**/mcp/**`, installer/config-schema/prompt source

문서 전용, test-fixture, `.omo/evidence/**` 편집은 연결된 것으로 보지 않습니다(게이트를 작동시키면 안 됨).

---

## 7. 우회 + 감사(D9)

- 표면: **필수 사유**를 담는 명시적 턴별 플래그입니다(예: MCP tool `evidence_bypass({reason})` 또는 인식되는 prompt marker. 정확한 표면은 계획에서 결정).
- 동작: 현재 턴에만 `ledger.bypass = {reason, at}`를 설정합니다.
- 게이트: 우회 시 `{session_id, reason, at, fresh_item_count, dirty_paths}`를 audit log(예: `.omo/evidence/_audit/bypass.log`)에 추가한 뒤, 다음 완료에는 신선한 재진술이 필요하도록 **자동 clear**합니다.
- 의도적으로 비영속: `gate.skipEvidence=true` config도, sticky env var도 없습니다.

---

## 8. 연결 지도(현재 OMC 소스 기준으로 재검증)

| 위치 | 역할 | 기존 sibling / 모델 |
|---|---|---|
| `packages/evidence-gate-core/`(새로 추가) | ledger I/O, sha256, 연결 경로 matcher, 신선도, 결정, 우회+감사 | `comment-checker-core`, `lsp-core`, `boulder-state` |
| `packages/omo-opencode/src/hooks/evidence-collector/` | PostToolUse(write/edit/apply_patch, Bash) -> ledger 업데이트 | `comment-checker`, `lsp`(둘 다 PostToolUse) |
| `packages/omo-opencode/src/hooks/evidence-gate/` | Stop, SubagentStop -> `{decision:block}` | `start-work-continuation`(이미 Stop/SubagentStop block) |
| `packages/omo-codex/...` | 둘 다 `postToolUse` / `stop` event용 Codex 컴포넌트로 등록 | codex component model(`hook/started`/`hook/completed`) |
| hook composition | 둘 다 5-tier hook composition(`create-hooks.ts`)에 연결 | 기존 component registration |

hooks.json matcher는 snake_case(`stop`, `subagent_stop`, `post_tool_use`)를 사용합니다. component CLI는 kebab(`hook stop`)을 사용합니다. `hook/*`의 camelCase notification eventNames(`stop`, `postToolUse`)를 사용합니다.

---

## 9. 검증 계획(수용 기준)

기존 QA harness를 재사용합니다. **수용 = 음성/양성 쌍이 통과**(gjc completion-gate test shape):

- **단위(결정적):** `scripts/hook-unit-probe.sh --component evidence-gate --event stop`
  - dirty + 신선한 증거 없음 -> 반드시 `{"decision":"block"}` 방출(음성)
  - dirty + 해시가 일치하는 passing item -> 반드시 allow(양성)
  - not dirty -> 반드시 allow
  - stale evidence(test 통과 후 파일 편집) -> 반드시 block
- **라이브(OpenCode):** `scripts/app-server-drive.sh --plugin --expect stop`
  - 연결 파일을 편집하고 test 없이 완료 시도 -> `hook/completed`(stop) + block 표면화
  - passing test 실행 후 완료 -> allow
- **라이브(Codex):** `bun run test:codex`를 컴포넌트 suite로 확장합니다. `scripts/app-server-drive.sh --plugin`은 `stop`에 대한 `hook/completed`를 확인합니다.
- **증거:** 모든 QA run은 OMC 의무에 따라 `.omo/evidence/<YYYYMMDD>-evidence-gate/`에 기록합니다.

---

## 10. ralplan에서 해결할 미해결 질문

1. 정확한 우회 표면(MCP tool vs prompt marker vs 둘 다)과 audit log 위치.
2. 최종 연결 경로 glob 집합 + D8 자동 캡처를 위한 "verification command" 패턴 감지 방식(cmd allowlist vs exit-code-only).
3. `evidence-collector`와 `evidence-gate`를 두 컴포넌트로 둘지, 두 event handler를 가진 하나의 컴포넌트로 둘지.
4. 두 Stop blocker가 충돌하지 않도록 `start-work-continuation`과의 상호작용(compose/order)을 정하는 방법.
5. Codex adapter: PostToolUse가 OpenCode와 같은 방식으로 Bash exit code를 노출하는가? 그렇지 않다면 D8 fallback.
6. migration/rollout: 첫 release에서 default-on으로 둘지 config flag 뒤에 둘지.

---

## 11. 참조(grounding - 재검증)

- OMC 증거 의무: `part7_opensource/oh-my-openagent/AGENTS.md`(QA-is-mandatory section, `.omo/evidence/` rule).
- 기존 Stop/SubagentStop blocker: `start-work-continuation`(component table, `.agents/skills/codex-qa/references/components-hooks.md`).
- PostToolUse components: `comment-checker`, `lsp`(같은 component table).
- PreToolUse deny 선례: `ulw-loop` `permissionDecision:"deny"`의 `create_goal` 적용.
- Codex hook 증명: `.agents/skills/codex-qa/references/app-server.md`(`hook/started`/`hook/completed`, eventNames).
- 패턴 출처(gjc): `ORCHESTRATION-MODES-GJC-VS-OMC.md` 섹션 4.5, Part 6 #2; `AI_AGENT_HARNESS_VIEW.md`.
