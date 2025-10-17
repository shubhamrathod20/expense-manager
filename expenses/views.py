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
    return render(request, 'expenses/expense_list.html', { 'expenses': expenses })


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
    total_spent = expenses.aggregate(total=Sum('amount'))['total'] or 0

    # Spending by category
    category_data = (
        expenses.values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    categories = [item['category'] for item in category_data]
    category_totals = [float(item['total']) for item in category_data]

    # Monthly spending trend
    monthly_data = (
        expenses.annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    months = [item['month'] for item in monthly_data]
    monthly_totals = [float(item['total']) for item in monthly_data]

    context = {
        'total_spent': total_spent,
        'categories': json.dumps(categories),
        'category_totals': json.dumps(category_totals),
        'months': json.dumps(months),
        'monthly_totals': json.dumps(monthly_totals),
    }

    return render(request, 'expenses/dashboard.html', context)

