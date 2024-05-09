from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .views import CustomAuthToken, LogoutView, ExpenseView, IncomeView, BalanceView, error_404_view, \
    ShopListView, AddIncomeView, index, StatisticView, AddExpenseView, home

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path('', auth_views.LoginView.as_view(), name='login'),
                  path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'),
                       name='logout'),  # Ustawienie template_name
                  path('home/',home, name="home"),
                  path('api-auth/', include('rest_framework.urls')),
                  path('api/login/', CustomAuthToken.as_view(), name='api-login'),
                  path('api/userdata/', CustomAuthToken.as_view(), name="user_data"),
                  path('api/logout/', LogoutView.as_view(), name="api_logout"),
                  path('api/expenses/', ExpenseView.as_view(), name='expenses_action'),
                  path('api/income/', IncomeView.as_view(), name='income_action'),
                  path('api/balance/', BalanceView.as_view(), name='expenses_action'),
                  path("api/shoplist/", ShopListView.as_view(), name="add_shoplist"),
                  path("api/getshoplists/", ShopListView.as_view(), name="get_shoplists"),
                  path("api/add_income/", AddIncomeView.as_view(), name="add_income"),
                  path("api/statistics/", StatisticView.as_view(), name="stats"),
                  path("api/add_expense/", AddExpenseView.as_view(), name="add_expense")

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)

handler404 = error_404_view
