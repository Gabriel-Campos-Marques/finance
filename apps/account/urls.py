from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, CreditCardViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'credit-cards', CreditCardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
