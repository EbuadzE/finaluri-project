from django.urls import path
from .views import LogoutUserView,LoginUserView,RegistrationUserView,ProfileView

app_name = 'users'

urlpatterns = [
    path('logout/', LogoutUserView.as_view(), name='logout' ),
    path('login/', LoginUserView.as_view(), name='login' ),
    path('registration/', RegistrationUserView.as_view(), name='registration' ),
    path('profile/', ProfileView.as_view(), name='profile')


]