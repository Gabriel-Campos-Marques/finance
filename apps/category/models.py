from django.db import models
from apps.core.models import BaseModel

class Category(BaseModel):
    CATEGORY_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense')
    )
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    type = models.CharField(max_length=50, choices=CATEGORY_TYPES)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class CategoryMappingRule(BaseModel):
    MATCH_TYPES = (
        ('exact', 'Exact Match'),
        ('contains', 'Contains'),
        ('startswith', 'Starts With'),
        ('endswith', 'Ends With')
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='mapping_rules')
    pattern = models.CharField(max_length=255)
    match_type = models.CharField(max_length=50, choices=MATCH_TYPES)
    normalized_pattern = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.pattern} -> {self.category.name}"
