"""ChatBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from ChatBot import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rasachat/<str:inputValue>/', views.rasachat, name='rasachat'),
    path('',views.heropage,name='home'),#as we have to call this page impicitly
    path('send_email/',views.send_email,name='feedback'),
    path('chatpage/',views.chatpage,name='chat'),#static url
    path('buttonmsg/<str:buttonName>/',views.buttonmsg,name='buttonmsg'), #dynamic url if we dont know which value will be there the dont write it
    path('subbuttonmsg/<str:corekey>/<str:content>/',views.subbuttonmsg,name='subbuttonmsg'),
    path('adminp/', views.adminpage),
    path('adminp/add/',views.add),
    path('adminp/updateKeyword/',views.updateKeyword, name="updateKeyword"),
    path('adminp/updateAnswer/',views.updateAnswer, name="updateAnswer"),
    path('adminp/delete/',views.delete, name="delete"),
    path('adminp/majorA/', views.MajorKeywordAnalysis),
    path('adminp/AnalyticsKey1/<str:major>/', views.SubKeywordAnalysis),
    path('coreKeyword/',views.majorKeywordRetrival),
    path('keywordMsg/<str:selectedValue>/',views.keywordMsg,name='keywordMsg'),
    path('addElement/<str:subKeyVal>/<str:inputField>/<str:textField>/',views.addElement,name='addElement'),
    path('deleteElement/<str:subKeyVal>/<str:inputField>/',views.deleteElement,name='deleteElement'),
    path('updatedKey/<str:subKeyVal>/<str:inputField>/<str:updatedKey>/', views.keyupdate, name='updatedKey'),
    path('updatedAns/<str:subKeyVal>/<str:inputField>/<str:updatedAnswer>/', views.ansupdate, name='updatedAns'),
    path('adminp/jsonList/', views.jsonList),
        #paths for registration
    path('signup/',views.Signuppage,name='signup'),
    path('login/',views.Loginpage,name='login'),
    path('superlogin/',views.super_login,name='superlogin'),
    path('log/',views.Logoutpage,name='logout'),
    path('token/',views.Tokenpage,name='tokenpage'),
    path('verify/<auth_token>',views.verify,name='verify'),
    
        #paths for reset password
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)