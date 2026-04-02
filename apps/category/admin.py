from django.contrib import admin, messages
from django.utils.translation import ngettext
from dateutil.relativedelta import relativedelta
from .models import Category, CategoryMappingRule, CategoryBudget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'parent', 'is_active')
    search_fields = ('name',)
    list_filter = ('type', 'is_active')

@admin.register(CategoryMappingRule)
class CategoryMappingRuleAdmin(admin.ModelAdmin):
    list_display = ('pattern', 'category', 'match_type', 'is_active')
    search_fields = ('pattern', 'normalized_pattern', 'category__name')
    list_filter = ('match_type', 'is_active')
    raw_id_fields = ('category',)

@admin.register(CategoryBudget)
class CategoryBudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'month', 'is_active')
    list_filter = ('month', 'category', 'is_active')
    search_fields = ('category__name',)
    actions = ['copy_to_next_month']

    @admin.action(description='Copiar para o próximo mês')
    def copy_to_next_month(self, request, queryset):
        created_count = 0
        for budget in queryset:
            next_month = budget.month + relativedelta(months=1)
            obj, created = CategoryBudget.objects.get_or_create(
                category=budget.category,
                month=next_month,
                defaults={'amount': budget.amount, 'is_active': budget.is_active}
            )
            if created:
                created_count += 1
        
        self.message_user(request, ngettext(
            '%d orçamento copiado com sucesso para o próximo mês.',
            '%d orçamentos copiados com sucesso para o próximo mês.',
            created_count,
        ) % created_count, messages.SUCCESS)
