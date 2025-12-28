from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from .models import Expense
from .forms import ExpenseForm
import json


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    total_income = expenses.filter(type='Income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = expenses.filter(type='Expense').aggregate(total=Sum('amount'))['total'] or 0

    balance = total_income - total_expense

    context = {
        'expenses': expenses,
        'balance': balance,
        'total_income': total_income,
        'total_expense': total_expense,
    }
    return render(request, 'expenses/expense_list.html', context)


@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense added successfully ✅")
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/add_expense.html', { 'form': form })


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated succeessfully ✏️")
            return redirect('expense_list')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'expenses/edit_expense.html', { 'form': form, 'expense': expense })


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        messages.warning(request, "Expense deleted 🗑️")
        return redirect('expense_list')
    return render(request, 'expenses/confirm_delete.html', { 'expense': expense })


@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)

    # Total spending
    total_income = expenses.filter(type='Income').aggregate(total=Sum('amount'))['total'] or 0
    total_spent = expenses.filter(type='Expense').aggregate(total=Sum('amount'))['total'] or 0

    balance = total_income - total_spent

    # Spending by category
    expense_category_data = (
        expenses.filter(type='Expense')
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    expense_categories = [item['category'] for item in expense_category_data]
    expense_category_totals = [float(item['total']) for item in expense_category_data]

    # Income by category
    income_category_data = (
        expenses.filter(type='Income')
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    income_categories = [item['category'] for item in income_category_data]
    income_category_totals = [float(item['total']) for item in income_category_data]

    # Monthly spending trend
    expense_monthly_data = (
        expenses.filter(type='Expense')
        .annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    expense_months = [item['month'] for item in expense_monthly_data]
    expense_monthly_totals = [float(item['total']) for item in expense_monthly_data]

    # Monthly income trend
    income_monthly_data = (
        expenses.filter(type='Income')
        .annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    income_months = [item['month'] for item in income_monthly_data]
    income_monthly_totals = [float(item['total']) for item in income_monthly_data]

    context = {
        'balance': balance,
        'total_income': total_income,
        'total_spent': total_spent,
        
        'expense_categories': json.dumps(expense_categories),
        'expense_category_totals': json.dumps(expense_category_totals),
        'income_categories': json.dumps(income_categories),
        'income_category_totals': json.dumps(income_category_totals),

        'expense_months': json.dumps(expense_months),
        'expense_monthly_totals': json.dumps(expense_monthly_totals),
        'income_months': json.dumps(income_months),
        'income_monthly_totals': json.dumps(income_monthly_totals)
    }

    return render(request, 'expenses/dashboard.html', context)

