from datetime import datetime

import requests
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from FinanseDjango.models import *
from django.utils import timezone
from datetime import timedelta


# Create your views here.


def home(request):
    return render(request, 'index.html')


@login_required
def homepage(request):
    user = request.user
    response = requests.get('https://api.quotable.io/random')
    data = response.json()
    quote_text = data['content']
    quote_author = data['author']
    context = {
        'quote_text': quote_text,
        'quote_author': quote_author,
        'user': user
    }

    return render(request, 'home/homepage.html', context)


@login_required
def incomes_view(request):
    user = request.user
    incomes = Income.objects.filter(user=user.id)
    paginator = Paginator(incomes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'incomes': incomes,
        'page_obj': page_obj
    }
    return render(request, 'home/incomes/index.html', context)


@login_required
def expenses_view(request):
    user = request.user
    expenses = Expense.objects.filter(user=user.id)
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'expenses': expenses,
        'page_obj': page_obj
    }
    return render(request, 'home/expenses/index.html', context)


@login_required
def wallet_view(request):
    user = request.user
    monthly_report = {}
    for month in range(1, 13):
        month_name = datetime.strptime(str(month), "%m").strftime("%B")
        translated_month_name = _(month_name)  # Tłumaczenie nazwy miesiąca

        total_income = Income.objects.filter(user=user.id, date__month=month).aggregate(total=Sum('amount'))[
                           'total'] or 0
        total_expense = Expense.objects.filter(user=user.id, date__month=month).aggregate(total=Sum('amount'))[
                            'total'] or 0
        balance = total_income - total_expense
        monthly_report[month] = {
            'name': translated_month_name,
            'incomes': total_income,
            'expenses': total_expense,
            'balance': balance
        }
    total_income = Income.objects.filter(user=request.user).aggregate(
        total=Coalesce(Sum('amount'), 0, output_field=DecimalField())
    )['total']
    total_expense = Expense.objects.filter(user=request.user).aggregate(
        total=Coalesce(Sum('amount'), 0, output_field=DecimalField())
    )['total']
    total_amount = total_income - total_expense
    analysis_results = analyze_monthly_balances(user)
    context = {
        'incomes': total_income,
        'expenses': total_expense,
        'balance': total_amount,
        'report': monthly_report,
        'analysis_results': analysis_results

    }
    return render(request, 'home/wallet/index.html', context)


def analyze_monthly_balances(user):
    now = timezone.now()
    current_month_start = now.replace(day=1)
    previous_month_end = current_month_start - timedelta(days=1)
    previous_month_start = previous_month_end.replace(day=1)

    # Sumy przychodów i wydatków w bieżącym miesiącu
    current_month_incomes = Income.objects.filter(date__gte=current_month_start, user=user.id).aggregate(Sum('amount'))['amount__sum'] or 0
    current_month_expenses = Expense.objects.filter(date__gte=current_month_start, user=user.id).aggregate(Sum('amount'))['amount__sum'] or 0

    # Sumy przychodów i wydatków w poprzednim miesiącu
    previous_month_incomes = Income.objects.filter(date__gte=previous_month_start, date__lte=previous_month_end).aggregate(Sum('amount'))['amount__sum'] or 0
    previous_month_expenses = Expense.objects.filter(date__gte=previous_month_start, date__lte=previous_month_end).aggregate(Sum('amount'))['amount__sum'] or 0

    # Porównanie przychodów
    if current_month_incomes > previous_month_incomes:
        income_comparison = "current_month_higher"
    elif current_month_incomes < previous_month_incomes:
        income_comparison = "current_month_lower"
    else:
        income_comparison = "same"

    # Porównanie wydatków
    if current_month_expenses > previous_month_expenses:
        expense_comparison = "current_month_higher"
    elif current_month_expenses < previous_month_expenses:
        expense_comparison = "current_month_lower"
    else:
        expense_comparison = "same"

    return {
        'income_comparison': income_comparison,
        'expense_comparison': expense_comparison,
        'current_month_incomes': current_month_incomes,
        'current_month_expenses': current_month_expenses,
        'previous_month_incomes': previous_month_incomes,
        'previous_month_expenses': previous_month_expenses
    }