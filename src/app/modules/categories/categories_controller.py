from nest.core import Controller, Get
from .categories_service import CategoriesService
from .dto.dto_categories import CategoryListResponse
from typing import List
from app.shared.config.config import API_PREFIX


@Controller(f"{API_PREFIX}/categories")
class CategoriesController:
    def __init__(self, categories_service: CategoriesService):
        self.categories_service = categories_service

    @Get("/")
    def get_all_categories(self) -> List[CategoryListResponse]:
        return self.categories_service.get_all_categories()
