from django import forms
from .models import Income, ExpenseCategory, Expense
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'source']

    amount = forms.DecimalField(
        label='Amount',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        required=True
    )

    source = forms.CharField(
        label='Source',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )


class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        fields = ['name']

    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'category', 'amount', 'date']

    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    category = forms.ModelChoiceField(
        label='Category',
        queryset=ExpenseCategory.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False
    )

    amount = forms.DecimalField(
        label='Amount',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    date = forms.DateField(
        label='Date',
        widget=forms.DateInput(attrs={'class': 'form-control'}),
        required=True
    )


class ExpenseFilterForm(forms.Form):
    year = forms.IntegerField(required=False)
    month = forms.CharField(required=False)
    reset = forms.BooleanField(widget=forms.HiddenInput(), required=False)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
