from django import forms
from django.core.exceptions import ValidationError
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'type', 'category', 'date', 'description']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    
                }
            ),
            'description': forms.Textarea(attrs={'rows': 2}),
        }

        def clean(self):
            cleaned_data = super().clean()
            type_ = cleaned_data.get('type')
            category = cleaned_data.get('category')

            if type_ and category:
                expense_categories = [c[0] for c in Expense.EXPENSE_CATEGORIES]
                income_categories = [c[0] for c in Expense.INCOME_CATEGORIES]

                if type_ == 'Income' and category not in income_categories:
                    raise ValidationError("Please select an income category for an income entry.")
                
                if type_ == 'Expense' and category not in expense_categories:
                    raise ValidationError("Please select an expense category for an expense entry.")
                
            return cleaned_data

        