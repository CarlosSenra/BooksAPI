from nest.core import Controller, Get
from .health_service import HealthService
from .dto.health_dto import HealthDto
from typing import List
from app.shared.config.config import API_PREFIX


@Controller(f"{API_PREFIX}/health")
class HealthController:
    def __init__(self, health_service: HealthService):
        self.health_service = health_service

    @Get("/")
    def get_health(self) -> HealthDto:
        return self.health_service.get_health()
