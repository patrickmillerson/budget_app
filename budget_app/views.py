import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.db.models import Sum
from django.utils import timezone
from .models import Income, ExpenseCategory, Expense
from django.views.decorators.csrf import csrf_protect
from .forms import ExpenseFilterForm, IncomeForm, ExpenseCategoryForm, ExpenseForm, SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Min, Max
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'budget_app/home.html')


@login_required
def income_list(request):
    # Get distinct years with incomes
    available_years = Income.objects.filter(user=request.user).dates('date', 'year').distinct()

    # Get the current year
    current_year = timezone.now().year

    # Get incomes for the current year
    incomes = Income.objects.filter(user=request.user, date__year=current_year)

    # Calculate total yearly income
    total_yearly_income = Income.objects.filter(user=request.user, date__year=current_year).aggregate(Sum('amount'))['amount__sum'] or 0

    # Include the selected year in the context
    selected_year = request.GET.get('year', current_year)

    # Get incomes for the selected year
    incomes_selected_year = Income.objects.filter(user=request.user, date__year=selected_year)

    return render(request, 'budget_app/income_list.html', {
        'incomes': incomes,
        'total_yearly_income': total_yearly_income,
        'current_year': current_year,
        'available_years': available_years,
        'selected_year': selected_year,
        'incomes_selected_year': incomes_selected_year,
    })
    
    
@login_required
def create_income(request):
    # Create income instance
    if request.method == 'POST':
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        source = request.POST.get('source')

        if amount and date:
            income = Income.objects.create(
                user=request.user,
                amount=amount,
                date=date,
                source=source
            )
            return redirect('income_list')

    return render(request, 'budget_app/create_income.html')


@login_required
def edit_income(request, id):
    # Edit income instance
    income = Income.objects.get(id=id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        source = request.POST.get('source')

        # Check if there are changes to the income
        if not amount == income.amount or not date == income.date or not source == income.source:
            income.amount = amount
            income.date = date
            income.source = source
            income.save()
            
            return redirect('income_list')

    context = {
        "income":income
    }
    return render(request, 'budget_app/edit_income.html', context)


@login_required
def expense_list(request):
    # Get the current year
    current_year = timezone.now().year

    # Default values
    selected_year = None
    selected_month = None

    # Initialize form with default values
    form = ExpenseFilterForm(request.GET or {'year': current_year, 'month': None})

    # Filter expenses based on user and current year
    expenses = Expense.objects.filter(user=request.user, date__year=current_year)

    # Calculate total expenses for the current year
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    if form.is_valid():
        # Extract user-selected values
        selected_year = form.cleaned_data['year']
        selected_month = form.cleaned_data['month']

        # Update expenses based on user-selected values
        if selected_year:
            expenses = Expense.objects.filter(user=request.user, date__year=selected_year)

            # If a month is selected, further filter by month
            if selected_month:
                try:
                    selected_month = datetime.datetime.strptime(selected_month, "%B").month
                    expenses = expenses.filter(date__month=selected_month)
                except ValueError:
                    pass

            # Recalculate total expenses based on user-selected filters
            total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'form': form,
        'expenses': expenses,
        'years': Expense.objects.filter(user=request.user).dates('date', 'year', order='DESC').distinct(),
        'months': Expense.objects.filter(user=request.user).dates('date', 'month', order='DESC').distinct(),
        'selected_year': selected_year,
        'selected_month': selected_month,
        'total_expenses': total_expenses,
    }

    return render(request, 'budget_app/expense_list.html', context)


@login_required
def create_expense(request):
    # Create an expense instance
    categories = ExpenseCategory.objects.filter(user=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        if name and category_id and amount and date:
            category = ExpenseCategory.objects.get(id=category_id)
            expense = Expense.objects.create(
                user=request.user,
                category=category,
                name=name,
                description=description,
                amount=amount,
                date=date
            )
            return redirect('expense_list')

    return render(request, 'budget_app/create_expense.html', {'categories': categories})

@login_required
def expense_category_list(request):
    # View for displaying expense categories
    categories = ExpenseCategory.objects.filter(user=request.user)
    return render(request, 'budget_app/expense_category_list.html', {'categories': categories})


@login_required
def create_expense_category(request):
    # Create an category instance
    if request.method == 'POST':
        name = request.POST.get('name')

        if name:
            expense_category = ExpenseCategory.objects.create(
                user=request.user,
                name=name
            )
            return redirect('expense_category_list')

    return render(request, 'budget_app/create_expense_category.html')


@login_required
def get_months(request):
    # Function that get only months that have expense
    selected_year = request.GET.get('year')

    if selected_year:
        # Get distinct months with expenses for the selected year
        months_with_expenses = Expense.objects.filter(
            user=request.user,
            date__year=selected_year
        ).dates('date', 'month', order='DESC').distinct()

        # Convert month numbers to month names (e.g., 1 -> 'January')
        month_names = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]

        # Include months only if there are expenses for that month
        months_html = [
            f'<option value="{month_names[month.month-1]}">{month_names[month.month-1]}</option>'
            for month in months_with_expenses
        ]

        # Add an option for no specific month (an empty option)
        months_html.insert(0, '<option value="">All</option>')

        return JsonResponse(months_html, safe=False)

    return JsonResponse([], safe=False)


def signup(request):    
    # Signup view
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page
            return redirect('signin')
        elif not form.is_valid():
            print(form.errors)
    else:
        form = SignUpForm()
        
        return render(request, 'budget_app/signup.html', {'form': form})



@csrf_protect
def signin_view(request):
    if request.method == 'POST':
        # We are using Django's built-in AuthenticationForm to validate the user's credentials
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # Getting the username and password from the form
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Log the user in
                login(request, user)
                messages.success(request, 'You have successfully signed in.')
                # Redirecti after successful login
                return redirect('expense_list')
            else:
                print('Invalid username or password')
                messages.error(request, 'Invalid username or password.')
                
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
                
    else:
        form = AuthenticationForm()

    return render(request, 'budget_app/signin.html', {'form': form})
 

def logout_view(request):
    logout(request)
    
    return redirect('home')