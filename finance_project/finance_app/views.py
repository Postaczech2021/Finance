
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Income, Outcome, Category
from django.db.models import Sum, Count
from .forms import IncomeForm, OutcomeForm, CategoryForm

def index(request):
    return render(request, 'index.html')

def statistics(request):
    categories = Category.objects.filter(name__icontains='nákup')
    total_amount = Outcome.objects.filter(category__in=categories).aggregate(Sum('amount'))['amount__sum'] or 1  # Ochrana proti dělení nulou

    outcomes_by_category = {}

    for category in categories:
        outcomes = Outcome.objects.filter(category=category)
        total_items = outcomes.aggregate(Count('id'))['id__count']
        total_spent = outcomes.aggregate(Sum('amount'))['amount__sum'] or 0
        percentage_of_total = (total_spent / total_amount) * 100

        outcomes_by_category[category.name] = {
            'outcomes': outcomes,
            'total_items': total_items,
            'total_spent': total_spent,
            'percentage_of_total': percentage_of_total,
        }

    context = {
        'outcomes_by_category': outcomes_by_category,
        'total_amount': total_amount,
    }

    return render(request, 'statistics.html', context)


def add_income(request):

    form = IncomeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        form = IncomeForm()

    income_all = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'add_income.html', {'form': form, 'income_all': income_all})


def add_outcome(request):
    form = OutcomeForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        form = OutcomeForm()

    outcome_all = Outcome.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'add_outcome.html', {'form': form, 'outcome_all': outcome_all})


def list_transactions(request):
    incomes = Income.objects.all()
    outcomes = Outcome.objects.all()

    total_income = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_outcome = Outcome.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'incomes': incomes,
        'outcomes': outcomes,
        'no_incomes': not incomes.exists(),
        'no_outcomes': not outcomes.exists(),
        'total_income': total_income,
        'total_outcome': total_outcome,
    }

    return render(request, 'list.html', context)


def edit_income(request, income_id):
    income = get_object_or_404(Income, id=income_id)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('list_transactions')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'edit_income.html', {'form': form})

def delete_income(request, income_id):
    income = Income.objects.get(pk=income_id)
    income.delete()
    return redirect('list_transactions')

def edit_outcome(request, outcome_id):
    outcome = get_object_or_404(Outcome, id=outcome_id)
    if request.method == 'POST':
        form = OutcomeForm(request.POST, instance=outcome)
        if form.is_valid():
            form.save()
            return redirect('list_transactions')
    else:
        form = OutcomeForm(instance=outcome)
    return render(request, 'edit_outcome.html', {'form': form, 'outcome': outcome})

def delete_outcome(request, outcome_id):
    outcome = Outcome.objects.get(pk=outcome_id)
    outcome.delete()
    return redirect('list_transactions')


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
