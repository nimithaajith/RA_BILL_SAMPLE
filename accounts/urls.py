from django.urls import path,include,reverse_lazy
from . views import *
from django.contrib.auth import views as auth_views
app_name='accounts'
urlpatterns = [
    path('',LoginView,name='UserLogin'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html',success_url=reverse_lazy('accounts:PasswordResetDone'),
            email_template_name='accounts/password_reset_email.html',),name='PasswordReset'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='PasswordResetDone'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',success_url=reverse_lazy('accounts:PasswordResetComplete')),name='PasswordResetConfirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='PasswordResetComplete'),
    path('email_exists',ajax_email_exists,name='EmailExists'),
    path('email_exists_edit',ajax_email_exists_edit,name='EmailExistsEdit'),
    path('accounts/logout/', userlogout),
    path('accounts/login/', LoginView),
]
