from django.contrib.auth.models import User
from django.db import models

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    source = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.amount

class ExpenseCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def extract_month(self):
        return f'{self.date.month}'

    def extract_year(self):
        return self.date.year
