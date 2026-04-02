from rest_framework import serializers
from .models import Category, CategoryMappingRule, CategoryBudget

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryMappingRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMappingRule
        fields = '__all__'

class CategoryBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryBudget
        fields = '__all__'
