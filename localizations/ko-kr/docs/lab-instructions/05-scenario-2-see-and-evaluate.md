# 시나리오 2 — 관찰하고 평가하기 (~10분)

아키텍처 다이어그램은 대개 오래되었거나, 틀렸거나, 아예 존재하지 않습니다. AI는 이를 즉석에서 생성할 수 있습니다 — 그런데 정확할까요?

## Part A — 다이어그램 생성하기 (~4분)

**Copilot에 입력:**

```
내 resource group의 리소스를 아키텍처 다이어그램으로 시각화해 줘.
```

### 5️⃣ `azure-resource-visualizer`가 활성화됩니다

이 skill이 어떻게 동작하는지 지켜보세요.
- Azure Resource Graph를 쿼리해 resource group 안의 모든 리소스를 목록화합니다
- 관계를 매핑합니다: Container App → Container Apps Environment → Log Analytics, Container App → ACR
- 레이블이 달린 subgraph, 리소스 유형, 연결 화살표가 포함된 Mermaid 다이어그램을 생성합니다
- 어떤 Mermaid 뷰어에도 붙여넣을 수 있는 렌더링 가능한 markdown을 출력합니다

> 💡 **Skill 집중 조명:** visualizer는 단순히 리소스를 나열하는 데 그치지 않습니다. 리소스 속성에서 관계를 추론합니다(예: `environmentId`가 Container App을 해당 Environment에 연결). 이름으로 추측하는 것이 아니라 ARM 리소스 모델을 읽습니다. 다만 Cosmos DB 의존성 같은 일부 연결은 ARM 리소스 속성이 아니라 Container App의 환경 변수를 통해서만 발견할 수 있으므로, visualizer가 이를 자동으로 포착하지 못할 수 있습니다.

> 💡 **Cosmos DB는 어떻게 되나요?** 여러분의 앱은 다른 resource group에 있을 수 있는 미리 프로비저닝된 Cosmos DB에 연결합니다. visualizer가 이 resource group 간 의존성을 포착하는지, 아니면 배포의 resource group 안 리소스만 보여 주는지 확인하세요. 이것은 자동 생성 다이어그램에서 흔히 나타나는 격차입니다.

---

## Part B — 다이어그램 평가하기 (~6분)

생성된 markdown을 열어 비판적으로 검토하세요.

- 배포된 리소스(Container App, Environment, ACR, Log Analytics)를 포착했나요?
- 관계가 올바른가요? ACR → Container App 풀을 보여 주나요?
- Cosmos DB 의존성을 보여 주나요? 그렇지 않다면 중대한 누락입니다 — 앱은 이것 없이는 동작하지 않습니다.
- 프로덕션 아키텍처 검토에 필요한데 빠진 것은 무엇인가요?

**Copilot에 입력:**

```
이 아키텍처에서 프로덕션 배포에 빠진 것은 무엇이야? 이 앱은 데이터를 위해 기존 Cosmos DB에도 연결해.
```

AI의 권장 사항을 시나리오 1B에서 여러분이 직접 찾아낸 결과와 비교하세요.

✅ **체크포인트:** 연결 화살표와 함께 배포된 리소스를 보여 주는 Mermaid 다이어그램을 확보했습니다. 렌더링하려면 Copilot 출력의 Mermaid 블록을 복사해 [mermaid.live](https://mermaid.live)에 붙여넣거나, Mermaid 확장이 설치된 VS Code를 사용하거나, markdown 파일을 GitHub 저장소에 커밋하세요 — GitHub는 markdown 파일의 Mermaid 다이어그램을 기본으로 렌더링합니다.

**핵심 교훈:** `azure-resource-visualizer`는 발견("지금 무엇이 존재하는가?")에는 탁월하지만, 문서화("이것이 완전하고 정확한가?")에는 전문가의 검토가 필요합니다. 다이어그램은 resource group 안에 배포된 상태를 반영할 뿐 전체 그림을 보여 주지 않습니다 — Cosmos DB 연결 같은 resource group 간 의존성은 여러분이 직접 문서화해야 합니다.

---

**다음:** [시나리오 3 — 파괴하고 진단하기 →](06-scenario-3-break-and-triage.md)
