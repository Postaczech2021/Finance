from django import forms
from .models import Income, Outcome, Category

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'amount','category']

class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['name', 'amount', 'category']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
