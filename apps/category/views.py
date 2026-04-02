from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Category, CategoryMappingRule, CategoryBudget
from .serializers import CategorySerializer, CategoryMappingRuleSerializer, CategoryBudgetSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class CategoryMappingRuleViewSet(viewsets.ModelViewSet):
    queryset = CategoryMappingRule.objects.all()
    serializer_class = CategoryMappingRuleSerializer
    permission_classes = [IsAuthenticated]

class CategoryBudgetViewSet(viewsets.ModelViewSet):
    queryset = CategoryBudget.objects.all()
    serializer_class = CategoryBudgetSerializer
    permission_classes = [IsAuthenticated]
