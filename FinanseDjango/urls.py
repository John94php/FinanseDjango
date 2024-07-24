from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from htmlApp import views as html_views

from .views import CustomAuthToken, LogoutView, ExpenseView, IncomeView, BalanceView, error_404_view, \
    ShopListView, AddIncomeView, StatisticView, AddExpenseView, index, EditProfile
urlpatterns = [
                  path("admin/", admin.site.urls),
                  path('', include('htmlApp.urls')),
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
                  path("api/add_expense/", AddExpenseView.as_view(), name="add_expense"),
                  path("api/edituserdata/", EditProfile.as_view(), name="edit_userdata")


              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)

handler404 = error_404_view
