from django.db import models
from django.contrib.auth.models import User

class Expense(models.Model):
    EXPENSE_CATEGORIES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Shopping', 'Shopping'),
        ('Bills', 'Bills'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
    ]

    INCOME_CATEGORIES = [
        ('Salary', 'Salary'),
        ('Bonus', 'Bonus'),
        ('Gift', 'Gift'),
        ('Refund', 'Refund'),
        ('OtherIncome', 'Other Income'), 
    ]

    ALL_CATEGORIES = INCOME_CATEGORIES + EXPENSE_CATEGORIES

    TYPE_CHOICES = [
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=ALL_CATEGORIES)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Expense')

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"
