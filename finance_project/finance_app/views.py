
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Income, Outcome, Category
from django.db.models import Sum
from .forms import IncomeForm, OutcomeForm, CategoryForm
from django.core.cache import cache

def index(request):
    return render(request, 'index.html')

def add_income(request):
    cache.clear()
    income_all = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            form = IncomeForm()
            income_all = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    else:
        form = IncomeForm()
        print(form.fields['category'].queryset)  # Přidáno pro kontrolu
    return render(request, 'add_income.html', {'form': form,'income_all':income_all})

def add_outcome(request):
    cache.clear()
    outcome_all = Outcome.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    if request.method == 'POST':
        form = OutcomeForm(request.POST)
        if form.is_valid():
            form.save()
            form =OutcomeForm()
            outcome_all = Outcome.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    else:
        form = OutcomeForm()
    return render(request, 'add_outcome.html', {'form': form,'outcome_all':outcome_all})

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
            return redirect('list')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'edit_income.html', {'form': form})

def delete_income(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    if request.method == 'POST':
        income.delete()
        return redirect('list')
    return render(request, 'confirm_delete.html', {'item': income})

def edit_outcome(request, outcome_id):
    outcome = get_object_or_404(Outcome, id=outcome_id)
    if request.method == 'POST':
        form = OutcomeForm(request.POST, instance=outcome)
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = OutcomeForm(instance=outcome)
    return render(request, 'edit_outcome.html', {'form': form})

def delete_outcome(request, outcome_id):
    outcome = get_object_or_404(Outcome, id=outcome_id)
    if request.method == 'POST':
        outcome.delete()
        return redirect('list')
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

def edit_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('manage_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form})

def delete_category(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        category.delete()
        return redirect('manage_categories')
    return render(request, 'delete_category.html', {'category': category})
