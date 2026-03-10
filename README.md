# LabPilot

PRD 기반 개인 R&D 엔지니어링 허브의 초기 백엔드 스캐폴드입니다.

## 현재 포함 범위

- FastAPI 애플리케이션 기본 구조
- `Project`, `ExperimentLog`, `HardwareIssue`, `Attachment` 데이터 모델
- 프로젝트, 실험 로그, 하드웨어 이슈 CRUD API
- 프로젝트 활동 요약 및 통합 타임라인 API
- PostgreSQL 기반 Docker Compose 실행 환경
- SQLite 기반 API 테스트

## 실행

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

기본 문서는 `/docs` 에서 확인할 수 있습니다.

## Docker Compose

```bash
docker compose up --build -d
```

API 서버는 `http://localhost:8000`, PostgreSQL은 `localhost:5432`로 노출됩니다.

## Testing

로컬 환경에 Python 패키지를 설치하지 않고 Docker 컨테이너 내부에서 테스트를 실행할 수 있습니다.
최상위 디렉토리에 있는 `test.sh` 스크립트를 사용하세요:

```bash
# 실행 권한 부여 (최초 1회)
chmod +x test.sh

# 테스트 실행
./test.sh
```

또는 직접 Docker 명령어를 사용할 수 있습니다:
```bash
docker compose exec api pytest
```

## CI/CD

- CI: GitHub Actions에서 `python -m compileall app tests`, `python -m pytest`, `docker compose config -q`, `docker build`
- CD: `main` 브랜치와 `v*` 태그 푸시 시 GHCR(`ghcr.io/<owner>/<repo>`)로 Docker 이미지를 푸시
