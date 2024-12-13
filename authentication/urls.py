from django.urls import path
from authentication.apis import GetConnectedView, RegisterClientView, LoginView, TokenRefreshView, \
    UpdateClientView, CompleteClientView, ResetPasswordRequestView, ResetPasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register-account/', RegisterClientView.as_view(), name='register'),
    path('update-account/', UpdateClientView.as_view(), name='update_account'),
    path('complete-account/', CompleteClientView.as_view(), name='complete_account'),
    path('password-reset/request/', ResetPasswordRequestView.as_view(), name='request_reset_pass'),
    path('password-reset/confirm/', ResetPasswordView.as_view(), name='confirm_reset_pass'),
    path('get-connected/', GetConnectedView.as_view(), name='get_connected'),
]
