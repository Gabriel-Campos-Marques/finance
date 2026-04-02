from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CategoryMappingRuleViewSet, CategoryBudgetViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'mapping-rules', CategoryMappingRuleViewSet)
router.register(r'budgets', CategoryBudgetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
