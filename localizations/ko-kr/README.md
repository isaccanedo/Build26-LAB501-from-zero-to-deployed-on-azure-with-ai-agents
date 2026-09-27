<p align="center">
<img src="../../img/banner-build-26.png" alt="Microsoft Build 2026" width="1200"/>
</p>

# [Microsoft Build 2026](https://build.microsoft.com)

## 🔥 LAB501: AI 에이전트와 함께 Azure에 처음부터 배포까지

### 사용 언어 선택

[English](../../README.md) | 한국어

> [!NOTE]
> 더 많은 언어를 곧 지원할 예정입니다!

### 세션 설명

AI에게 빌드를 맡기면 어떤 일이 벌어질까요? 이 핸즈온 랩에서는 빈 터미널에서 시작해 Azure에 앱을 배포하는 전 과정을 직접 경험합니다. GitHub Copilot CLI와 coding agent가 스캐폴딩, 코딩, 디버깅, 배포를 모두 처리합니다. 새로운 Azure skill을 사용해 자연어만으로 리소스를 프로비저닝하고 서비스를 연결하며, 포털은 전혀 사용하지 않습니다. 이 세션은 단순히 지켜보는 데모가 아닙니다. 여러분은 다음 프로젝트에 바로 가져갈 수 있는 실제 작동하는 개발 워크플로를 손에 쥐고 나갑니다.

75분(Level 300) 동안 단일 Copilot 프롬프트로 두 개의 서비스를 배포합니다. Azure Container Apps 위에서 동작하는 Python **Flask LEGO set browser**와, LEGO set을 Azure Cosmos DB에 배치 upsert하는 Python **Azure Function App**입니다. 그런 다음 아키텍트의 관점으로 AI의 결정을 평가합니다. 생성된 Bicep을 검토하고, managed identity와 RBAC로 배포를 강화하며, 일부러 망가뜨린 뒤 KQL로 전체 포렌식 조사를 수행합니다. 이 모든 작업을 GitHub Copilot CLI에서 진행합니다.

### 🏫 가이드 세션으로 시작하기

가이드 랩 세션에서 시작하려면 다음 단계를 따르세요.

- Skillable 랩 VM에 로그인한 다음 **Docker Desktop**을 실행합니다
- PowerShell을 열고 `az login`, `azd auth login`, `copilot`을 차례로 실행한 뒤, [로그인 및 실행](docs/lab-instructions/02-login-and-launch.md)을 따라 **Azure Skills** 플러그인을 설치합니다(`/plugin install azure@azure-skills`)
- [랩 개요](docs/lab-instructions/00-overview.md)를 따라가며 네 가지 시나리오를 순서대로 진행합니다

### 🏠 내 환경에서 시작하기

각자의 속도에 맞춰 이 단계를 따라간다면 다음과 같이 진행하세요.

- 저장소를 복제합니다: `git clone https://github.com/microsoft/Build26-LAB501.git`
- [사전 준비물](docs/lab-instructions/01-prerequisites.md)을 설치합니다: Python 3.13+, Docker Desktop, Git, Azure CLI(및 Bicep), Azure Developer CLI(`azd`), GitHub Copilot CLI, 그리고 Contributor 권한을 가진 Azure 구독
- LEGO 데이터셋이 담긴 Azure Cosmos DB를 직접 프로비저닝한 뒤(database `LegoDatabase`, container `legoSets`), [스타터 앱 설정](docs/lab-instructions/03-getting-started.md)부터 시작해 네 가지 시나리오를 진행합니다

### 🧠 학습 성과

이 세션을 마치면 다음을 할 수 있습니다.

- GitHub Copilot CLI에서 단일 자연어 프롬프트로 Azure skill(`azure-prepare` → `azure-validate` → `azure-deploy`)을 연결해 IaC, Docker, 구성을 스캐폴딩하고 컨테이너화된 앱을 Azure에 배포하기
- AI가 생성한 Bicep, Dockerfile, 아키텍처 다이어그램을 비판적으로 검토해 프로덕션 격차를 찾아내고, `azure-rbac`와 `azure-resource-visualizer`로 least-privilege managed identity와 정확한 문서를 통해 그 격차를 메우기
- `azure-diagnostics`로 프로덕션 문제를 진단하고 운영화하기 — 시스템 로그에서 근본 원인까지 이어지는 추론 과정을 따라간 다음, 사후 분석을 Azure 포털을 한 번도 열지 않고 KQL 쿼리와 경고 규칙으로 전환하기

### 💬 Copilot으로 계속 학습하기

다음 프롬프트를 GitHub Copilot에 사용해 이 세션의 주제를 더 깊이 탐구해 보세요. VS Code에서 Copilot Chat을 열고(Windows/Linux는 `Ctrl+Alt+I`, Mac은 `Cmd+Shift+I`) 프롬프트를 붙여넣은 뒤 무엇을 배우는지 확인하세요. 최신 공식 문서를 활용하려면 [Microsoft Learn MCP Server](#-microsoft-learn-mcp-server)를 연결해 보세요.

이 프롬프트를 출발점으로 삼거나, 직접 작성해도 좋습니다.

- "Python Flask 앱을 Azure Container Apps에 배포하고, 동시에 Python Azure Function App을 Bicep과 `azd`로 스캐폴딩해 줘. ACR 풀과 Cosmos DB 접근에는 managed identity를 사용해."
- "내 Container App Bicep에서 프로덕션 준비 격차를 검토해 줘 — managed identity, RBAC, VNet integration, diagnostic settings, health probe를 확인하고 수정안을 제안해."
- "데이터를 읽기만 하는 앱을 위한 최소 권한 Cosmos DB RBAC 역할을 찾아서 `az cosmosdb sql role assignment create` 명령을 생성해 줘."
- "내 resource group의 리소스를 Mermaid 아키텍처 다이어그램으로 시각화해 줘. Cosmos DB처럼 다른 resource group에 걸친 의존성도 포함해."
- "내 Container App이 503을 반환해. 시스템 로그를 가져와 ingress 구성과 연관 지어 근본 원인과 해결책을 알려줘."
- "`ContainerAppSystemLogs_CL`을 대상으로 첫 번째 `ProbeFailed` 이벤트와 다음 `RevisionReady` 이벤트 사이의 다운타임을 계산하는 KQL 쿼리를 작성한 뒤, 이를 `az monitor scheduled-query create` 경고 규칙으로 전환해 줘."

### 💻 사용 기술

1. GitHub Copilot CLI + Azure Skills 플러그인(`azure-prepare`, `azure-validate`, `azure-deploy`, `azure-rbac`, `azure-resource-visualizer`, `azure-diagnostics`)과 Azure MCP Server
2. Azure Container Apps, LEGO set 배치 수집을 위한 **Azure Functions(Python, Flex Consumption)**, Azure Container Registry, managed identity + RBAC를 적용한 Azure Cosmos DB(NoSQL)
3. Azure Developer CLI(`azd`), Bicep, Docker, Python 3.13 / Flask, Azure Monitor + Log Analytics, KQL

### 📚 리소스 및 다음 단계

| 리소스 | 설명 |
|:---------|:------------|
| [https://aka.ms/build26-next-steps](https://aka.ms/build26-next-steps) | Build 2026 이후 학습 여정의 다음 단계로 나아가기 |
| [랩 개요](docs/lab-instructions/00-overview.md) | 아키텍처 다이어그램, skill 맵, 섹션별 랩 가이드 |
| [다음 단계](docs/lab-instructions/09-whats-next.md) | 확장 아이디어 — private endpoint, VNet integration, Key Vault, OIDC 기반 CI/CD, Terraform |
| [Azure Skills 플러그인 발표](https://devblogs.microsoft.com/all-things-azure/announcing-the-azure-skills-plugin/) | 랩 전반에서 사용하는 Azure skill에 대한 배경 설명 |
| [Azure MCP Server 문서](https://learn.microsoft.com/azure/developer/azure-mcp-server) | Azure skill을 구동하는 MCP 도구 레퍼런스 |
| [GitHub Copilot CLI 문서](https://docs.github.com/en/copilot/github-copilot-in-the-cli) | GitHub Copilot CLI 설치, 구성, 확장 |
| [Container Apps 배포 및 관리](https://learn.microsoft.com/training/paths/deploy-manage-container-apps) | Azure Container Apps용 Microsoft Learn 학습 경로 |
| [Azure Cosmos DB 문서](https://learn.microsoft.com/azure/cosmos-db) | Cosmos DB의 데이터 모델링, RBAC, 운영 가이드 |


### 🌟 Microsoft Learn MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Microsoft_Docs_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D)

Microsoft Learn MCP Server는 GitHub Copilot 같은 클라이언트와 여러 AI 에이전트가 Microsoft 공식 문서의 신뢰할 수 있는 최신 정보를 직접 가져오도록 돕는 원격 MCP Server입니다. 위의 원클릭 버튼으로 VS Code에 설치하거나, 이 저장소에 포함된 [mcp.json](../../.vscode/mcp.json) 파일을 사용해 시작하세요.

자세한 정보, 다른 개발 클라이언트용 설정 안내, 의견 및 질문은 Learn MCP Server GitHub 저장소 [https://github.com/MicrosoftDocs/MCP](https://github.com/MicrosoftDocs/MCP)에서 확인하세요. 에이전트를 연결할 다른 MCP Server는 [https://mcp.azure.com](https://mcp.azure.com)에서 찾아보세요.

*참고: Learn MCP Server를 사용하면 [Microsoft Learn](https://learn.microsoft.com/en-us/legal/termsofuse) 및 [Microsoft API 약관](https://learn.microsoft.com/en-us/legal/microsoft-apis/terms-of-use)에 동의하는 것입니다.*

## 콘텐츠 소유자

<!-- TODO: Add yourself as a content owner
1. Change the src in the image tag to {your github url}.png
2. Change INSERT NAME HERE to your name
3. Change the github url in the final href to your url. -->

<table>
<tr>
    <td align="center"><a href="http://github.com/yunjchoi">
        <img src="https://github.com/yunjchoi.png" width="100px;" alt="Yun Jung Choi"/><br />
        <sub><b>Yun Jung Choi</b></sub></a><br />
            <a href="https://github.com/yunjchoi" title="talk">📢</a>
    </td>
</tr></table>

## 기여하기

이 프로젝트는 기여와 제안을 환영합니다. 대부분의 기여는 여러분이 해당 기여를 사용할 권리를 실제로 보유하고 있으며 그 권리를 당사에 부여한다고 선언하는 Contributor License Agreement(CLA) 동의를 필요로 합니다. 자세한 내용은 [Contributor License Agreements](https://cla.opensource.microsoft.com)를 참고하세요.

pull request를 제출하면 CLA 봇이 CLA 제공 여부를 자동으로 판단하고 PR에 적절히 표시합니다(예: 상태 확인, 코멘트). 봇이 안내하는 지침을 따르기만 하면 됩니다. CLA를 사용하는 모든 저장소에서 이 작업은 한 번만 하면 됩니다.

이 프로젝트는 [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/)를 채택했습니다. 자세한 내용은 [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)를 참고하거나, 추가 질문이나 의견이 있으면 [opencode@microsoft.com](mailto:opencode@microsoft.com)으로 문의하세요.

## 상표

이 프로젝트는 프로젝트, 제품, 서비스의 상표나 로고를 포함할 수 있습니다. Microsoft 상표나 로고의 정당한 사용은 [Microsoft 상표 및 브랜드 가이드라인](https://www.microsoft.com/legal/intellectualproperty/trademarks/usage/general)을 따라야 합니다. 이 프로젝트를 수정한 버전에서 Microsoft 상표나 로고를 사용할 때는 혼동을 일으키거나 Microsoft의 후원을 암시해서는 안 됩니다. 제3자 상표나 로고의 사용은 해당 제3자의 정책을 따릅니다.
