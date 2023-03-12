from django.urls import path
from . import views
urlpatterns = [
    # Post Routes
    path("register",views.user_register,name='user_register'),
    path('logout',views.user_logout,name="user_logout")

]