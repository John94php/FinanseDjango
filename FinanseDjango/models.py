from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ShopList(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    items = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "shoplist"


class Income(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "income"


class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_file = models.FileField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    expense_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "expense"
