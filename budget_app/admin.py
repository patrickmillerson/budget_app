from django.contrib import admin

from budget_app.models import Expense, ExpenseCategory, Income

# Register your models here.

admin.site.register(Income)
admin.site.register(ExpenseCategory)
admin.site.register(Expense)