from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
                  path('', views.home, name='home'),
                  path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
                  path('password-reset/',
                       auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
                       name='password_reset'),
                  path('main/', views.homepage, name='homepage'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('incomes/', views.incomes_view, name='incomes'),
                  path('expenses/', views.expenses_view, name='expenses'),
                  path('wallet/', views.wallet_view, name='wallet'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
