# 시나리오 3 — 파괴하고 진단하기 (~10분)

새벽 2시입니다. 여러분의 앱이 503을 반환합니다. 터미널을 엽니다. 답만이 아니라 AI의 진단 추론 과정에 주목하세요.

## 장애 일으키기

`<app>`과 `<rg>`를 시나리오 1A에서 만든 실제 Container App 이름과 resource group으로 바꾸세요(찾아야 한다면 `azd env get-values`를 실행하세요). 그런 다음 새 PowerShell 탭에서 다음 명령을 실행하세요.

```powershell
az containerapp ingress update --name <app> -g <rg> --target-port 9999
```

> ⏱️ **이 명령은 새 Container Apps 리비전이 활성화되는 동안 ~30초에서 2분이 걸립니다.** 예상된 동작이니 Ctrl+C를 누르지 마세요.

엔드포인트에 요청하면 `503 Service Unavailable`이 나옵니다.

---

## AI로 진단하기

**Copilot에 입력:**

```
내 Container App이 503을 반환해. 뭐가 문제야?
```

### 6️⃣ `azure-diagnostics`가 활성화됩니다

triage 과정을 지켜보세요.

1. **가설 수립** — skill은 여러 장애 유형을 고려합니다: 앱 충돌? ingress 구성 오류? 잘못된 이미지? 비정상 environment?
2. **로그 조회** — `az containerapp logs show --type system`을 사용해 Container App 시스템 로그를 가져옵니다
3. **로그 상관 분석** — `Reason: ProbeFailed`를 찾아냅니다 — *"Probe of StartUp failed with status code: 1"*(컨테이너가 포트 9999에서 수신 대기하지 않아 startup probe가 실패합니다)
4. **구성 검증** — ingress 구성(포트 9999)을 컨테이너의 수신 포트(Dockerfile에서 gunicorn이 설정한 8000)와 대조합니다
5. **근본 원인 + 해결책** — 올바른 포트를 복원하는 정확한 CLI 명령을 제시합니다

> 💡 **Skill 집중 조명:** `azure-diagnostics`는 단순히 로그에서 오류를 검색하지 않습니다. 진단 추론 과정을 따릅니다. 넓게 시작해(무엇이 503을 일으킬 수 있는가?) 증거로 좁히고(시스템 로그에 ProbeFailed가 보인다) 구성 데이터로 확인합니다. 이는 시니어 SRE가 따르는 것과 동일한 triage 패턴입니다.

---

## 해결책 적용하기

제안된 해결 명령을 실행하세요. 다음과 비슷할 것입니다.

```powershell
az containerapp ingress update --name <app> -g <rg> --target-port 8000
```

복구를 확인하세요 → `200 OK`.

✅ **체크포인트:** `curl <your-endpoint-url>`이 다시 LEGO set browser HTML을 반환합니다.

**핵심 교훈:** 자연어 질문 하나 → `azure-diagnostics` 활성화 → ~30초 만에 근본 원인 + 해결책. 이 skill이 평소 포털에서 수동으로 하던 로그 상관 분석을 대신했습니다.

---

**다음:** [시나리오 4 — 조사하고 운영화하기 →](07-scenario-4-investigate-and-operationalize.md)
