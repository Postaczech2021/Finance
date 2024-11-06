
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Income, Outcome, Category
from django.db.models import Sum, Count, Avg
from .forms import IncomeForm, OutcomeForm, CategoryForm
from django.utils import timezone

def index(request):
    return render(request, 'index.html')

def statistics(request):
    categories = Category.objects.filter(name__icontains='nákup')
    total_amount = Outcome.objects.filter(category__in=categories).aggregate(Sum('amount'))['amount__sum'] or 1
    outcomes_by_category = {}

    # Statistiky pro výdaje
    total_items_all = 0
    for category in categories:
        outcomes = Outcome.objects.filter(category=category)
        total_items = outcomes.aggregate(Count('id'))['id__count']
        total_spent = outcomes.aggregate(Sum('amount'))['amount__sum'] or 0
        avg_spent = outcomes.aggregate(Avg('amount'))['amount__avg'] or 0
        percentage_of_total = (total_spent / total_amount) * 100
        outcomes_by_category[category.name] = {
            'outcomes': outcomes,
            'total_items': total_items,
            'total_spent': total_spent,
            'avg_spent': avg_spent,
            'percentage_of_total': percentage_of_total,
        }
        total_items_all += total_items

    # Seřadit kategorie podle celkové útraty (od nejvyšší k nejnižší)
    sorted_outcomes_by_category = dict(
        sorted(outcomes_by_category.items(), key=lambda item: item[1]['total_spent'], reverse=True))

    # Statistiky pro příjmy
    total_income_amount = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 1
    income_stats = Income.objects.aggregate(
        total_amount=Sum('amount'),
        avg_amount=Avg('amount'),
        count=Count('id')
    )

    # Bilance mezi příjmy a výdaji
    balance = (total_income_amount - total_amount) / total_income_amount * 100

    context = {
        'outcomes_by_category': sorted_outcomes_by_category,
        'total_amount': total_amount,
        'total_income_amount': total_income_amount,
        'income_stats': income_stats,
        'total_items_all': total_items_all,
        'balance': balance,
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
    if request.method == 'POST':
        form = OutcomeForm(request.POST)
        if form.is_valid():
            form.save()

            # Uchování zadaného data a kategorie do session
            request.session['last_date'] = form.cleaned_data['date'].isoformat()
            request.session['last_category'] = form.cleaned_data['category'].id

            return redirect('add_outcome')
    else:
        # Načtení zadaného data a kategorie ze session, pokud existují
        initial_data = {
            'date': request.session.get('last_date', timezone.now().date()),
            'category': request.session.get('last_category', Category.objects.first().id)
        }
        form = OutcomeForm(initial=initial_data)

    outcome_all = Outcome.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    return render(request, 'add_outcome.html', {'form': form, 'outcome_all': outcome_all})


def prepare_context(shopname=None):
    incomes = Income.objects.all()
    categories = Category.objects.filter(is_income=False)
    total_income = Income.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    total_outcome = Outcome.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    category = None
    outcomes = []
    outcomes_count = 0

    if shopname:
        category = Category.objects.filter(name=shopname).first()
        outcomes = Outcome.objects.filter(category=category.id) if category else []
        outcomes_count = outcomes.count() if category else 0

    context = {
        'incomes': incomes,
        'outcomes': outcomes,
        'categories': categories,
        'category': category,
        'shopname': shopname,
        'total_income': total_income,
        'total_outcome': total_outcome,
        'outcomes_count': outcomes_count,
        'total_outcomes_count': Outcome.objects.count(),
        'no_incomes': not incomes.exists(),
        'no_outcomes': not outcomes.exists() if shopname else False,
    }
    return context

def list_transactions(request):
    context = prepare_context()
    return render(request, 'list.html', context)

def list_transactions_by_shop(request):
    shopname = request.GET.get('shopname')
    context = prepare_context(shopname=shopname)
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
