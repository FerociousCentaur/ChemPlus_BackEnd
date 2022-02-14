"""ChemPlus1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ChemID import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('loginAdmin/', views.login_view, name='login'),
    path('logoutAdmin/', views.logout_view, name='logout'),
    path('tableview/', views.return_table, name='secretpage'),
    path('downloaddata/<str:program>/', views.download_data, name='download'),
    path('checkiitm/', views.checkiitm, name='checkiitm'),
    path('', views.signup),
    #path('homepage/', views.homepage,name='home'),
    path('signupverify/<path:crypt_mail>', views.Verifier),
    path('resend/', views.resendOTP, name='resendOTP'),
    #path('payments/', views.payment_request, name='paymentpage'),
    path('payments/', views.comingsoon, name='paymentpage'),
    path('handleResponse/', views.handleResponse, name='handleResponse'),
    path('s2sresponse/', views.server_to_server, name='s2sresponse'),

]
