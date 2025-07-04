from nest.core import Module
from .health_controller import HealthController
from .health_service import HealthService


@Module(
    controllers=[HealthController],
    providers=[HealthService],
)
class HealthModule:
    pass
