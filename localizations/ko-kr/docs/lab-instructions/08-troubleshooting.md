# 문제 해결

## Cosmos DB 연결이 로컬에서 실패함
**증상:** `python app.py`가 인증 또는 연결 오류를 보여 줍니다.
**원인:** 앱이 `DefaultAzureCredential`을 사용하는데, 이는 활성화된 Azure CLI 로그인이 필요합니다.
**해결:** `az login`을 실행하고 올바른 구독에 있는지 확인하세요. `.env`의 `COSMOS_ENDPOINT`가 프로비저닝된 Cosmos DB와 일치하는지 확인하세요.

## ACR 이름에 하이픈이 포함됨 → 배포 실패
**증상:** `azd up`이 잘못된 ACR 이름 오류로 실패합니다.
**원인:** ACR 이름은 영숫자여야 합니다. AZD 환경 이름의 하이픈이 레지스트리 이름으로 전파됩니다.
**해결:** 하이픈이 없는 환경 이름(예: `lab501app`)을 사용하세요. 새 이름으로 `azd init`을 다시 실행하세요.

## AZD가 잘못된 구독에 배포함
**증상:** 예상치 못한 구독에 리소스가 나타나거나 권한 오류가 발생합니다.
**원인:** AZD는 `az account show`와 별개로 자체 구독 구성을 유지합니다.
**해결:** `azd env set AZURE_SUBSCRIPTION_ID $(az account show --query id -o tsv)`를 실행해 정렬하세요.

## 배포 후 Container App이 Cosmos DB에 연결하지 못함
**증상:** 앱이 배포되지만 접근 시 데이터베이스 오류를 보여 줍니다.
**원인:** Container App이 Cosmos DB에 도달할 적절한 권한이나 환경 변수를 갖추지 못했습니다.
**해결:** Container App에 `COSMOS_ENDPOINT`, `COSMOS_DATABASE`, `COSMOS_CONTAINER` 환경 변수를 설정했는지 확인하세요. managed identity를 사용한다면 system-assigned identity에 적절한 Cosmos DB RBAC 역할을 할당했는지 확인하세요.

## `az containerapp ingress update`가 2분 이상 멈춰 있음
**증상:** 명령이 실행 후 멈춘 것처럼 보입니다.
**원인:** CLI가 새 Container Apps 리비전이 활성화되기를 기다립니다.
**해결:** 예상된 동작입니다. 완료될 때까지 기다리세요 — Ctrl+C를 누르지 마세요.

## 배포 후 첫 요청이 타임아웃되거나 응답이 느림
**증상:** `curl`이 타임아웃되거나 첫 요청에 10초 이상 걸립니다.
**원인:** 새 리비전이 활성화 중입니다(cold start). `minReplicas: 1`을 설정해도 초기 활성화에는 시간이 걸립니다.
**해결:** 배포가 완료된 후 ~15초 기다린 뒤 다시 시도하세요.

## 시나리오 4에서 KQL 쿼리가 결과를 반환하지 않음
**증상:** 쿼리가 빈 테이블을 반환합니다.
**원인:** Log Analytics 수집에 ~5분의 지연이 있습니다. 메트릭은 ~15분의 지연이 있습니다.
**해결:** 시나리오 3 이후 5분 기다린 뒤 쿼리를 다시 시도하세요.

## `az monitor scheduled-query create`가 "command not found"로 실패함
**증상:** CLI가 `scheduled-query` 명령을 인식하지 못합니다.
**원인:** preview CLI 확장을 설치하지 않았습니다.
**해결:** `az extension add --name scheduled-query --yes`를 실행하세요.

## `azd up` 중 Docker 빌드가 실패함
**증상:** Docker 관련 오류로 배포가 실패합니다.
**원인:** Docker Desktop이 실행 중이 아닙니다.
**해결:** Docker Desktop을 시작하고 `docker version`으로 확인하세요. 그런 다음 `azd up`을 다시 실행하세요.

## Python 의존성 설치가 실패함
**증상:** `pip install -r requirements.txt`가 오류로 실패합니다.
**원인:** 시스템 의존성이 없거나 Python 버전이 잘못되었습니다.
**해결:** `python --version`으로 Python 3.13+를 실행 중인지 확인하세요. 먼저 `pip install --upgrade pip`를 시도해 보세요.

## KQL 쿼리에서 PowerShell 따옴표 이스케이프 문제
**증상:** KQL `where Reason_s == "ProbeFailed"`가 PowerShell에서 구문 오류로 실패합니다.
**원인:** PowerShell은 큰따옴표를 bash와 다르게 처리합니다.
**해결:** 대신 `has` 연산자를 사용하세요: `where Reason_s has "ProbeFailed"`. AI는 보통 이를 자동으로 처리합니다.

## 배포 후 Gunicorn 포트 불일치
**증상:** 새로 배포한 뒤에도 Container App이 503을 보여 줍니다.
**원인:** ingress target port가 gunicorn의 bind port(8000)와 일치하지 않습니다.
**해결:** Container App ingress target port를 `8000`(Dockerfile CMD `gunicorn --bind 0.0.0.0:8000`과 일치)으로 설정했는지 확인하세요.

---

**돌아가기:** [개요](00-overview.md) | [다음 단계 →](09-whats-next.md)
