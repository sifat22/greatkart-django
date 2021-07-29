from django.urls import path
from .import views

app_name='app_login'
urlpatterns=[

    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('',views.dashboard, name='dashboard'),


      #user activation

      path('activate/<uidb64>/<token>/',views.activate,name='activate'),

      #forgot password
      path('forgotpassword/',views.forgotpassword,name='forgot_password'),
      path('resetpassword_validate/<uidb64>/<token>/',views.resetpassword_validate,name='resetpassword_validate'),
      path('resetpassword/',views.resetpassword,name='resetpassword')

   

]