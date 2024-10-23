
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Income, Outcome, Category
from .forms import IncomeForm, OutcomeForm, CategoryForm

def index(request):
    return render(request, 'index.html')

def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})

def add_outcome(request):
    if request.method == 'POST':
        form = OutcomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = OutcomeForm()
    return render(request, 'add_outcome.html', {'form': form})

def list_transactions(request):
    incomes = Income.objects.all()
    outcomes = Outcome.objects.all()
    total_income = sum(income.amount for income in incomes)
    total_outcome = sum(outcome.amount for outcome in outcomes)
    balance = (total_income - total_outcome) / total_income * 100 if total_income else 0
    return render(request, 'list.html', {
        'incomes': incomes,
        'outcomes': outcomes,
        'balance': balance
    })


def edit_income(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('income_list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'edit_income.html', {'form': form})

def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    if request.method == 'POST':
        income.delete()
        return redirect('income_list')
    return render(request, 'confirm_delete.html', {'item': income})

def edit_outcome(request, outcome_id):
    outcome = get_object_or_404(Outcome, id=outcome_id)
    if request.method == 'POST':
        form = OutcomeForm(request.POST, instance=outcome)
        if form.is_valid():
            form.save()
            return redirect('outcome_list')
    else:
        form = OutcomeForm(instance=outcome)
    return render(request, 'edit_outcome.html', {'form': form})

def delete_outcome(request, outcome_id):
    outcome = get_object_or_404(Outcome, id=outcome_id)
    if request.method == 'POST':
        outcome.delete()
        return redirect('outcome_list')
    return render(request, 'confirm_delete.html', {'item': outcome})

def manage_categories(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm()
    return render(request, 'manage_categories.html', {'categories': categories, 'form': form})
