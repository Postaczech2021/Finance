from django import forms
from .models import Income, Outcome, Category

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['name', 'amount', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Název položky',
            'amount': 'Částka',
            'category': 'Kategorie',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_income=True).order_by('-name')

class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['name', 'amount', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
    
        }
        labels = {
            'name': 'Název výdajové položky',
            'amount': 'Částka',
            'category': 'Kategorie',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_income=False)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','is_income']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_income': forms.CheckboxInput(attrs={'class': 'form-check-input float-end '}),
            
        }
        labels = {
            'name':'Název kategorie',
            'is_income':'Pouze příjmová kategorie',
        }