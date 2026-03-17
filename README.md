# LabPilot — Backend

개인 R&D 프로젝트 관리를 위한 FastAPI 백엔드 서버입니다.
프로젝트, 실험 로그, 하드웨어 이슈, 첨부파일, 외부 저장소 연동 기능을 제공합니다.

---

## 기술 스택

| 항목 | 내용 |
|------|------|
| 언어 | Python 3.11+ |
| 프레임워크 | FastAPI |
| ORM | SQLAlchemy 2.x |
| DB (개발) | SQLite (`labpilot.db` 자동 생성) |
| DB (운영) | PostgreSQL 17 (Docker Compose) |
| 패키지 관리 | uv |
| 테스트 | pytest |

---

## 프로젝트 구조

```
app/
├── main.py              # FastAPI 앱 진입점 (CORS, 라우터 마운트)
├── core/
│   └── config.py        # 환경 설정 (pydantic-settings)
├── db/
│   └── session.py       # DB 엔진 및 테이블 초기화
├── models/              # SQLAlchemy ORM 모델
│   ├── project.py
│   ├── experiment_log.py
│   ├── hardware_issue.py
│   ├── attachment.py
│   ├── repository.py
│   └── enums.py
├── schemas/             # Pydantic 요청/응답 스키마
├── api/
│   └── routes/          # 라우터 (projects, experiment_logs, hardware_issues, attachments, repositories)
└── services/
    └── storage.py       # 파일 업로드 디렉토리 초기화
```

---

## 로컬 실행 (개발)

### 사전 준비
- Python 3.11 이상
- [uv](https://docs.astral.sh/uv/) 설치

### 실행

```bash
# 의존성 설치
uv sync --all-extras

# 서버 실행 (SQLite 자동 생성, 포트 8000)
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

API 문서: http://localhost:8000/docs
헬스체크: http://localhost:8000/health

---

## Docker Compose 실행 (운영)

PostgreSQL + API 서버를 함께 실행합니다.

```bash
docker compose up --build -d
```

| 서비스 | 포트 |
|--------|------|
| API 서버 | http://localhost:8000 |
| PostgreSQL | localhost:5432 |

---

## 테스트

```bash
# 로컬 (SQLite 임시 DB 사용)
uv run pytest

# Docker 컨테이너 내부
docker compose exec api pytest
```

---

## 주요 API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/projects` | 프로젝트 목록 |
| POST | `/api/projects` | 프로젝트 생성 |
| GET | `/api/projects/{id}` | 프로젝트 상세 |
| GET | `/api/projects/{id}/timeline` | 통합 타임라인 |
| GET/POST | `/api/projects/{id}/experiment-logs` | 실험 로그 |
| GET/POST | `/api/projects/{id}/hardware-issues` | 하드웨어 이슈 |
| POST | `/api/attachments` | 파일 첨부 |
| GET/POST | `/api/projects/{id}/repositories` | 외부 저장소 연동 |
| GET | `/health` | 헬스체크 |

---

## 환경 변수

`.env` 파일로 설정 가능합니다 (기본값으로도 동작).

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `DATABASE_URL` | `sqlite:///./labpilot.db` | DB 연결 문자열 |
| `UPLOAD_DIR` | `./uploads` | 파일 업로드 경로 |
| `APP_NAME` | `LabPilot` | 앱 이름 |

---

## CI/CD

- **CI**: GitHub Actions — `compileall`, `pytest`, `docker compose config`, `docker build`
- **CD**: `main` 브랜치 및 `v*` 태그 푸시 시 GHCR(`ghcr.io/<owner>/<repo>`)로 Docker 이미지 배포
