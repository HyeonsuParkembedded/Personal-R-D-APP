from fastapi import APIRouter

from app.api.routes import attachments, experiment_logs, hardware_issues, projects, repositories

api_router = APIRouter()
api_router.include_router(projects.router)
api_router.include_router(experiment_logs.router)
api_router.include_router(hardware_issues.router)
api_router.include_router(repositories.router)
api_router.include_router(attachments.router)
