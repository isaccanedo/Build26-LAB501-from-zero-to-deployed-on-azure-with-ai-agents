# 시나리오 1 — 배포하고 강화하기 (~35분)

AI는 몇 분 만에 Azure 배포를 스캐폴딩할 수 있습니다. 그런데 AI가 생성한 Bicep을 검토 없이 프로덕션에 푸시할 수 있을까요?

## Part A — 배포하기 (~25분)

> 💡 **앱이 현재 실행 중이 아닌지 확인하세요.** 체크포인트에서 `python app.py`를 시작했다면, 계속하기 전에 **Ctrl+C**로 중지하세요.

아직 **lego-set-browser** 디렉터리에 있지 않다면 그 안으로 cd한 다음, 아래 프롬프트로 **yolo mode**의 Copilot 세션을 시작하세요.

```
copilot --yolo
```

`--yolo` 플래그는 명령을 자동 승인하고 확인 프롬프트를 건너뜁니다. 랩은 샌드박스 환경에서 실행되므로 여기서는 안전하며, 랩을 진행하는 동안 몇 분을 절약해 줍니다. 그런 다음 Copilot에 입력하세요.

```
  Azure 서비스 2개를 생성하고 배포해 줘
   	
   **환경:**
   - 구독: 현재 구독
   - 새 resource group 생성: rg-lego-set-browser-dev
   - Region: West US 3
   
   **기존 Cosmos DB(새로 만들지 마):**
   - 현재 구독에서 기존 Cosmos DB를 찾아
   - Database: LegoDatabase / Container: legoSets
   
   **1. Python Azure Function App** — Flex Consumption(FC1)의 HTTP POST trigger:
   - LEGO set의 JSON 배열을 받아 위 Cosmos DB에 배치 upsert
   - 필드: set_number (→ id), name, theme_name, year_released, number_of_parts, type, image_url
   - Cosmos DB용 user-assigned managed identity(Built-in Data Contributor)
   
   **2. 이 폴더의 Flask 앱 → Azure Container Apps:**
   - 이름: ca-web-lego-<XXXX>
   - 이미 DefaultAzureCredential + 환경 변수 COSMOS_ENDPOINT, COSMOS_DATABASE, COSMOS_CONTAINER 사용
   - Cosmos DB용 system-assigned managed identity(Built-in Data Reader)
```

이 하나의 프롬프트가 **세 개의 skill 체인**을 트리거합니다 — Copilot이 각 skill을 호출하는 모습을 지켜보세요.

### 1️⃣ `azure-prepare`가 가장 먼저 활성화됩니다

이 skill이 **완전히 다른 두 시작점**을 한 번에 어떻게 처리하는지 지켜보세요 — 이것이 이 단계의 핵심 통찰입니다.

- **Flask 앱 → Container Apps(시작점: 워크스페이스의 기존 소스 코드):**
  - 워크스페이스를 스캔해 `requirements.txt`와 `app.py`를 찾고 Python Flask 웹 앱으로 분류합니다
  - 호스팅 대상으로 Container Apps를 선택합니다(App Service나 Functions 대신 이 선택에 동의하시나요?)
  - 기존 `Dockerfile`을 검토합니다(앱에 이미 하나가 있습니다 — skill이 그대로 쓰는지 다시 생성하는지 지켜보세요)
  - 이미 존재하는 코드 *주변에* 인프라를 생성합니다
- **Python Function App → Azure Functions(시작점: 프롬프트뿐 — 아직 소스 코드 없음):**
  - 워크스페이스에 function 코드가 없습니다. skill은 프롬프트(HTTP POST trigger, LEGO set의 JSON 배열, Cosmos DB로의 배치 upsert)를 읽고 **적합한 Azure Functions Python 템플릿을 가져옵니다**
  - 그 템플릿을 시나리오에 맞게 수정합니다. 핸들러를 LEGO JSON 형태를 받도록 다시 작성하고, `set_number → id`를 매핑하며, 기존 Cosmos DB 데이터베이스/컨테이너에 연결하고, user-assigned managed identity 바인딩을 추가합니다
  - 호스팅 플랜으로 **Flex Consumption(FC1)**을 선택하고 배포 패키지용 Storage 계정을 추가합니다
  - 템플릿을 바탕으로 인프라 *와* 소스 코드를 모두 생성합니다
- **두 서비스에 공통으로 적용되는 부분:**
  - 두 서비스를 선언하는 단일 `azure.yaml`과 `infra/`의 Bicep 템플릿(일반적으로 `main.bicep`과 서비스별 모듈)을 생성합니다
  - AZD 환경을 만들고 구독과 region을 설정합니다

> 💡 **Skill 집중 조명:** `azure-prepare`는 단순히 파일을 생성하는 데 그치지 않습니다. 여러분의 언어 런타임, Bicep 패턴, AZD 관례, Azure Functions Flex Consumption 템플릿에 대한 skill 레퍼런스를 읽습니다. 생성된 파일을 열어 보세요. `infra/`의 Bicep과 새 `function_app.py`는 일반적인 보일러플레이트가 아니라 skill 레퍼런스 템플릿에서 나온 것입니다.

### 2️⃣ 다음으로 `azure-validate`가 활성화됩니다

두 서비스에 걸쳐 사전 점검을 실행합니다.
- Container App과 Function App 모듈의 Bicep을 컴파일합니다(`az bicep build`) — 배포 전에 구문 오류를 잡아냅니다
- Docker가 실행 중인지 확인합니다 — Container App 이미지 빌드는 Docker 없이 실패합니다
- Python 런타임 버전과 선택한 region에서 Flex Consumption(FC1)이 사용 가능한지 확인합니다 — 그렇지 않으면 Functions 배포가 빠르게 실패합니다
- 구독 접근 권한과 resource group 이름이 사용 중이지 않은지 확인합니다

### 3️⃣ 마지막으로 `azure-deploy`가 활성화됩니다

`azd up --no-prompt`를 실행해 두 서비스를 하나의 오케스트레이션된 실행으로 프로비저닝하고 배포합니다.
- **Container App 쪽:** ACR, Container Apps Environment, Log Analytics, Container App을 프로비저닝하고, Docker 이미지를 빌드해 ACR에 푸시합니다
- **Function App 쪽:** Storage 계정, Flex Consumption(FC1) 플랜, user-assigned managed identity, Application Insights, Function App을 프로비저닝하고, Python function 코드를 패키징해 배포합니다
- Cosmos DB 환경 변수를 두 서비스에 연결하고 라이브 HTTPS 엔드포인트를 반환합니다(Flask UI용 Container Apps URL과 수집 엔드포인트용 Functions URL)

### 동작 확인하기

```bash
curl <your-endpoint-url>
```

> 💡 **엔드포인트 URL 찾기:** URL이 화면 밖으로 스크롤되어 사라졌다면 `azd env get-values`를 실행하거나 Copilot에 "What's the URL for my Container App?"이라고 물어보세요. URL은 `https://<app-name>.<region>.azurecontainerapps.io` 형태입니다.

> 💡 **첫 요청은 느릴 수 있습니다:** 배포 직후 첫 요청은 새 리비전이 활성화되는 동안 10~15초가 걸릴 수 있습니다. 정상적인 동작이니 잠시 후 다시 시도하세요.

> ⚠️ **Container App에서 Cosmos DB 접근:** 배포 후 Container App은 Cosmos DB에 접근할 권한이 필요합니다. 앱에서 데이터베이스 접근과 관련된 오류가 보이면 예상된 상황입니다 — Part B(강화하기)에서 적절한 Cosmos DB RBAC 역할로 managed identity를 구성해 이를 해결합니다.

**최종 상태:** LEGO set browser를 제공하는 라이브 HTTPS 엔드포인트입니다. 세 개의 skill, 하나의 프롬프트로 완성했습니다. 하지만 배포되었을 뿐, 아직 프로덕션 준비가 된 것은 아닙니다.

![브라우저에서 실행 중인 LEGO Vault 앱](../../../../docs/lab-instructions/images/workingApp.png)

> 📁 **어떤 파일이 생성되었나요?** Part A 이후 `lego-app` 디렉터리에는 `azure-prepare`가 생성한 새 파일이 있어야 합니다. 일반적으로 `azure.yaml`과 Bicep 템플릿이 담긴 `infra/` 폴더(예: `main.bicep`, `main.parameters.json`, 지원 모듈)입니다. 기존 `Dockerfile`은 그대로 유지되었거나 업데이트되었을 수 있습니다. 정확한 파일 구조는 AI가 프로젝트를 어떻게 스캐폴딩했는지에 따라 조금씩 달라질 수 있습니다.

---

## Part B — 강화하기 (~10분)

> ⚠️ **권한 참고:** 일부 강화 작업(예: managed identity용 역할 할당 생성)은 구독에 대한 **Owner** 또는 **User Access Administrator** 역할을 요구할 수 있습니다. 이 단계에서 권한 오류가 발생하면 일부 랩 환경에서는 예상된 상황입니다 — 모든 명령을 실행하기보다 패턴을 이해하고 AI의 권장 사항을 검토하는 데 집중하세요.

`infra/` 디렉터리의 생성된 Bicep 파일을 검토하세요. `azure-prepare`가 어떻게 실행되었는지에 따라 생성 과정에서 이미 일부 보안 강화를 적용했을 수 있습니다. 여러분의 임무는 **AI가 한 것과 하지 않은 것을 감사하는 일**입니다.

**Copilot에 입력:**

```
배포한 Container App 인프라에서 프로덕션 준비 격차를 검토해 줘. managed identity, (키 대신) Cosmos DB RBAC 접근, VNet integration, diagnostic settings, health probe를 확인해.
```

### 무엇을 확인해야 하나

| 격차 | 왜 중요한가 | 심각도 |
|---|---|---|
| **ACR 풀용 managed identity 없음** | Container App이 admin 자격 증명으로 이미지를 풀합니다. 보안 결함입니다. | 높음 |
| **Cosmos DB용 managed identity 없음** | 앱이 RBAC 대신 연결 키를 사용합니다. 키는 유출될 수 있습니다. | 높음 |
| **VNet integration 없음** | Container Apps Environment가 공용 네트워크에 있습니다. 격리가 없습니다. | 중간 |
| **diagnostic settings 없음** | 플랫폼이 메트릭을 전달하지 않습니다. CPU/메모리 경고를 놓칩니다. | 중간 |
| **health probe 미구성** | 기본값인 TCP probe를 사용합니다. 앱에 home 라우트가 있으니 그것을 사용해야 합니다. | 낮음 |

> 💡 **AI가 이미 일부를 강화했을 수 있습니다.** `azure-prepare` skill은 초기 생성 단계에서 managed identity와 RBAC를 설정하는 보안 강화 단계를 포함합니다. AI가 managed identity와 AcrPull을 이미 구성했다면 — 훌륭합니다. 의도대로 skill이 동작한 것입니다. 아직 빠진 부분, 특히 managed identity를 통한 Cosmos DB 접근에 검토를 집중하세요.

✅ **체크포인트:** 생성된 인프라를 감사했고, AI가 강화했음을 확인했거나 다음 단계를 찾아냈습니다. 이제 Container App은 ACR 이미지 풀과 Cosmos DB 데이터 접근 모두에 managed identity를 사용해야 합니다.

**핵심 교훈:** AI는 기본적으로 안전한 배포를 만들 수도, 그렇지 않을 수도 있습니다. skill의 보안 강화 단계는 비결정적이며, 바로 그래서 사람의 검토가 중요합니다. AI가 강화했든 여러분이 프롬프트로 지시했든, 핵심 역량은 "프로덕션 준비"가 어떤 모습인지 알고 그것을 검증하는 일입니다.

---

**다음:** [시나리오 2 — 관찰하고 평가하기 →](05-scenario-2-see-and-evaluate.md)
