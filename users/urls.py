from django.urls import path

from users.views import (
    LoginView, LogoutView, PasswordResetView,
    PasswordResetCompleteView, PasswordResetDoneView,
    PasswordResetConfirmView, AccountActivationSent, activate, SignupTypeView,SignupView, PendingActivationView
)


urlpatterns = [
    path('signup/type/', SignupTypeView.as_view(), name='signup-type'),
    path('signup/', SignupView.as_view(), name='signup'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset', PasswordResetView.as_view(),
         name='password_reset'),
    path('password_reset/done', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/',
         PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('account_activation_sent', AccountActivationSent.as_view(),
         name='account_activation_sent'),
    path('pending/activation/', PendingActivationView.as_view(),
         name='pending_activation'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
]
