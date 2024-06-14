import json
from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShopList, Income, Expense
from .serializers import EditProfileSerializer


def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


def index(request):
    return HttpResponse("Witaj w API Finanse!")


def error_404_view(request, exception):
    return render(request, '404.html', status=404)


class CustomAuthToken(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user
            data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'name': user.first_name,
                'surname': user.last_name
            }
            return Response(data)
        else:
            return Response({'error': 'Unauthorized'}, status=401)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.auth

        if token:
            token.delete()
            return Response({'message': 'Wylogowano pomyślnie.'})
        else:
            return Response({'error': 'Brak tokena JWT w nagłówku autoryzacji.'}, status=400)


class ExpenseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            current_user = request.user
            user_id = current_user.id
            list_of_expenses = Expense.objects.filter(user=user_id)
            serialized_expenses = []
            for expense in list_of_expenses:
                serialized_income = {
                    'id': expense.id,
                    'name': expense.name,
                    'amount': expense.amount,
                    'user_id': expense.user_id,
                    'date': expense.expense_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'expense_file': expense.expense_file.url
                }
                serialized_expenses.append(serialized_income)

            return JsonResponse({
                'data': serialized_expenses,
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    def post(self, request, *args, **kwargs):
        action = request.data.get('action')
        return Response({"message": f"Akcja {action} została wykonana dla wydatków"})


class IncomeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            current_user = request.user
            user_id = current_user.id
            list_of_incomes = Income.objects.filter(user=user_id)
            serialized_incomes = []
            for income in list_of_incomes:
                serialized_income = {
                    'id': income.id,
                    'name': income.name,
                    'amount': income.amount,
                    'user_id': income.user_id,
                    'date': income.income_date.strftime('%Y-%m-%d %H:%M:%S')
                }
                serialized_incomes.append(serialized_income)

            return JsonResponse({
                'data': serialized_incomes,
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })

    def post(self, request):
        action = request.data.get('action')
        return Response({"message": f"Akcja {action} została wykonana dla bilansu"})


class BalanceView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        total_income = Income.objects.filter(user=request.user).aggregate(
            total=Coalesce(Sum('amount'), 0, output_field=DecimalField())
        )['total']
        total_expense = Expense.objects.filter(user=request.user).aggregate(
            total=Coalesce(Sum('amount'), 0, output_field=DecimalField())
        )['total']
        total_amount = total_income - total_expense
        return Response({
            'amount': total_amount
        })


class StatisticView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def decimal_serializer(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    def get(self, request):
        monthly_report = {}
        for month in range(1, 13):
            month_name = datetime.strptime(str(month), "%m").strftime("%B")
            translated_month_name = _(month_name)  # Tłumaczenie nazwy miesiąca

            total_income = Income.objects.filter(income_date__month=month).aggregate(total=Sum('amount'))['total'] or 0
            total_expense = Expense.objects.filter(expense_date__month=month).aggregate(total=Sum('amount'))[
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

        return Response({
            'incomes': total_income,
            'expenses': total_expense,
            'balance': total_amount,
            'report': monthly_report
        })


class ShopListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        title = data.get('title')
        items = data.get('items')
        userId = data.get('userId')
        user = User.objects.get(pk=userId)

        # Przekształć listę elementów na ciąg tekstowy
        items_string = json.dumps(items)

        # Utwórz nowy obiekt ShopList i zapisz go do bazy danych
        shop_list = ShopList(name=title, items=items_string, user=user)
        shop_list.save()
        response_data = json.dumps([])
        response = HttpResponse(response_data, content_type='application/json')

        return response

    def get(self, request, *args, **kwargs):
        try:
            current_user = request.user
            user_id = current_user.id
            list_of_shoplists = ShopList.objects.filter(user=user_id)
            shoplists_data = [{
                'id': item.id, 'title': item.name, 'items': item.items} for item in list_of_shoplists]
            print(shoplists_data)
            return Response(shoplists_data)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })


class AddIncomeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        try:
            name = data['name']
            amount = data['amount']
            current_user = request.user
            user = User.objects.get(pk=current_user.id)
            income = Income(name=name, amount=amount, user=user)
            income.save()
            return Response({
                'message': 'Sukces',
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            })


class AddExpenseView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == 'POST' and request.FILES:
            try:
                name_input = request.data.get('name')
                amount_input = request.data.get('amount')
                date_input = request.data.get('date')
                uploaded_file = request.FILES.get('file')
                with open('media/' + uploaded_file.name, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                current_user = request.user
                user = User.objects.get(pk=current_user.id)
                new_expense = Expense(name=name_input, amount=amount_input, expense_file=uploaded_file,
                                      expense_date=date_input, user=user)
                new_expense.save()
                return JsonResponse({
                    'status': 'OK',
                    'code': '200'
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'ERROR',
                    'code': '500',
                    'message': str(e)
                })



        else:
            return JsonResponse({
                'error': 'Brak pliku'
            })


class EditIncomeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass


class EditProfile(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EditProfileSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.username = serializer.validated_data['username']
            user.email = serializer.validated_data['email']
            user.first_name = serializer.validated_data['name']
            user.last_name = serializer.validated_data['surname']
            user.save()
            return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def add_expense(request):
    if request.method == 'POST':
        amount = request.POST.get('expenseAmount')
        image = request.FILES.get('expenseImage')
        print(amount)
