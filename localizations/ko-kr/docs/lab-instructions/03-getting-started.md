# 시작하기 — 스타터 앱 설정

다음 안내에 따라 스타터 앱을 설정하세요.

## 1. 랩 저장소 복제하기

새 PowerShell 세션을 열고, 랩 저장소를 복제한 뒤 그 안으로 이동하세요.

```powershell
git clone https://github.com/microsoft/Build26-LAB501.git
```
```powershell
cd Build26-LAB501
```

## 2. 스타터 앱 복사하기

`src/` 디렉터리에는 바로 사용할 수 있는 Python Flask 애플리케이션이 있습니다 — Azure Cosmos DB를 백엔드로 하는 LEGO set browser입니다. 이를 새 `lego-set-browser` 작업 디렉터리로 복사하고 별도의 Git 저장소로 초기화하세요.

```powershell
Copy-Item -Recurse src lego-set-browser
```
```powershell
cd lego-set-browser
```
```powershell
git config --global user.name "Your Name"
```
```powershell
git config --global user.email "you@example.com"
```
```powershell
git init
```
```powershell
git add -A
```
```powershell
git commit -m "init"
```
문제가 생기면 명령을 직접 입력하고 한 번에 하나씩 실행해 보세요.

이후의 모든 명령은 `lego-set-browser` 디렉터리에서 실행하세요.

> 💡 **스타터 앱에는 무엇이 들어 있나요?** `app.py`는 LEGO set을 탐색, 검색, 조회하는 라우트를 갖춘 Flask 웹 애플리케이션입니다. Azure Cosmos DB에 연결해 set 데이터를 쿼리합니다. `requirements.txt`는 Python 의존성(Flask, azure-cosmos, azure-identity, gunicorn)을 정의합니다. 컨테이너 배포를 위한 `Dockerfile`도 함께 들어 있습니다. 이 앱은 Cosmos DB에 대한 암호 없는 인증을 위해 `DefaultAzureCredential`을 사용합니다.

## 3. 로컬 테스트

온사이트 랩에서는 랩을 끝낼 시간을 더 확보하기 위해 로컬 테스트를 의도적으로 건너뜁니다.

---

**다음:** [시나리오 1 — 배포하고 강화하기 →](04-scenario-1-ship-and-harden.md)
