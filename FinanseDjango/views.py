import json

from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import ShopList, Income, Expense
import json
import datetime
from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
import pytesseract
from PIL import Image
from rest_framework import status, serializers


def index(request):
    return render(request, 'index.html')


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
                    'income_date': income.income_date.strftime('%Y-%m-%d %H:%M:%S')  # Formatowanie daty
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
        action = request.data.get('action')
        return Response({"message": f"Akcja {action} została wykonana dla bilansu"})


class StatisticView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
            'balance': total_amount
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
        data = request.data
        if 'file' in data:
            file = data['file']
            self.handle_uploaded_file(file)
            return Response({
                'status': 'success',
                'data': 'Dane przesłane poprawnie'
            })
        else:
            return Response({
                'status': 'error',
                'message': 'Brak pliku w danych żądania'
            }, status=status.HTTP_400_BAD_REQUEST)


    def handle_uploaded_file(self, file):
        with open('images' + file.name, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)


class EditIncomeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pass
