# 시나리오 4 — 조사하고 운영화하기 (~15분)

장애가 해결되었습니다. 이제 질문합니다. "얼마나 오래 다운되었나? 다음번에는 어떻게 막을까?"

> ⏱️ **로그 수집 지연:** Container App 시스템 로그가 Log Analytics에 나타나기까지 ~5분이 걸립니다. 시나리오 3을 빠르게 끝냈다면 지금쯤 데이터가 준비되었을 것입니다 — 그렇지 않다면 1분 기다린 뒤 다시 시도하세요.

## Part A — KQL로 사후 분석하기 (~7분)

**Copilot에 입력:**

```
내 Container App의 Log Analytics workspace를 쿼리해 줘. port mismatch 장애 동안 무슨 일이 있었는지 보여 줘.
```

### 7️⃣ `azure-diagnostics`가 활성화됩니다

조사를 어떻게 구성하는지 지켜보세요.

1. **Workspace 탐색** — resource group에서 Log Analytics workspace를 찾습니다
2. **테이블 탐색** — `ContainerAppSystemLogs_CL`을 쿼리해 사용 가능한 이벤트 유형을 찾습니다
3. **이벤트 분포** — KQL `summarize count() by Reason_s`를 실행해 분포를 보여 줍니다: ProbeFailed 이벤트(잘못된 포트에서 startup probe 실패로 발생), ReplicaUnhealthy 영향, RevisionUpdate 복구
4. **장애 타임라인** — `earliest(TimeGenerated)`와 `latest(TimeGenerated)`를 사용한 KQL 쿼리를 작성해 정확한 다운타임 길이를 계산합니다
5. **복구 확인** — `RevisionReady` 이벤트를 확인해 수정이 효과가 있었음을 증명합니다

> 💡 **Skill 집중 조명:** `azure-diagnostics`는 자연어를 바탕으로 KQL을 *대신* 작성합니다. 생성된 쿼리를 검토하세요 — 여러분이라면 다르게 작성했을까요? 이 skill은 KQL의 문자열 매칭에 `==` 대신 `has`를 사용하는데, 이는 로그 형식 변화에 더 강합니다.

**AI가 작성한 KQL을 검토하세요.** 쿼리를 복사해 수정해 보세요 — `| where TimeGenerated > ago(1h)` 필터를 추가하거나, 시계열 보기를 위해 `summarize`를 `bin(TimeGenerated, 5m)`을 포함하도록 바꿔 보세요. 수정한 쿼리를 Copilot CLI에서 실행하거나 Azure 포털의 Log Analytics 쿼리 편집기에 붙여넣으세요.

✅ **체크포인트:** ProbeFailed 이벤트(포트 불일치로 발생), 장애 타임라인, 복구 확인을 보여 주는 KQL 쿼리를 확인했습니다.

---

## Part B — 운영화하기 (~8분)

> ⚠️ **참고:** 아래 단계는 기존 정책 제약 때문에 일부 랩 환경에서 실패할 수 있습니다. 그래도 시도해 보세요 — 성공하면 동작하는 경고 규칙을 얻게 됩니다. 실패하면 KQL과 경고 구성 패턴을 이해하는 데 집중하세요.

**Copilot에 입력:**

```
Container App 시스템 로그에 ProbeFailed 이벤트가 나타나면 발동하는 KQL 경고 규칙을 만들어 줘.
```

### `azure-diagnostics`가 계속됩니다

이 skill은 다음을 수행합니다.
- `ContainerAppSystemLogs_CL`을 대상으로 하는 경고 KQL 쿼리를 작성합니다
- threshold, frequency, severity, action group을 포함한 전체 `az monitor scheduled-query create` 명령을 생성합니다
- 각 매개변수를 설명해 여러분이 직접 조정할 수 있게 합니다(예: 평가 빈도, 발동 전 위반 횟수)

> ⚠️ **사전 조건:** `scheduled-query` CLI 확장을 먼저 설치해야 합니다: `az extension add --name scheduled-query --yes`

**그런 다음 질문하세요:**

```
Cosmos DB를 백엔드로 하는 프로덕션 Container App에 어떤 경고 규칙이 더 있어야 해?
```

AI는 다음을 제안합니다: replica health, restart loop, 높은 지연 시간, 5xx 급증, 메모리 사용률, Cosmos DB request unit 소비, throttling(429) — 각각 필요한 KQL 패턴과 함께 제시합니다.

✅ **체크포인트:** `az monitor scheduled-query list -g <rg> -o table`이 경고 규칙을 보여 줍니다.

**핵심 교훈:** 두 개의 프롬프트, 하나의 skill(`azure-diagnostics`)로 "장애가 끝났다"에서 "이 유형의 장애가 다음번에는 나를 호출할 것이다"로 나아갔습니다. 진정한 300 레벨 가치는 이것입니다. 이제 여러분은 이러한 KQL 쿼리를 직접 읽고 수정할 수 있습니다.

> 💡 **팁:** `az monitor scheduled-query create`의 `--condition` 매개변수는 raw KQL이 아니라 특정 DSL 형식을 사용합니다. condition은 KQL 쿼리의 테이블 이름(예: `ContainerAppSystemLogs_CL`)을 참조하고, 전체 KQL은 `--condition-query`에 들어갑니다. 명령이 실패하면 이 두 매개변수가 일관적인지 확인하세요.

---

**다음:** [문제 해결 →](08-troubleshooting.md)
