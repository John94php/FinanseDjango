from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import CustomPasswordChangeView

from . import views

urlpatterns = [
                  path('', views.home, name='home'),
                  path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
                  path('password_reset/',
                       auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
                       name='password_reset'),

                  path('password_reset/done/',
                       auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
                       name='password_reset_done'),
                  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
                      template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
                  path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
                      template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

                  path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),

                  path('main/', views.homepage, name='homepage'),
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('incomes/', views.incomes_view, name='incomes'),
                  path('expenses/', views.expenses_view, name='expenses'),
                  path('wallet/', views.wallet_view, name='wallet'),
                  path('userProfile/', views.profile_view, name='userProfile'),
                  path('set-theme/', views.set_theme, name='set_theme'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
