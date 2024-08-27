from django.contrib import admin
from django.urls import path
from app import views
from django.contrib.auth.views import PasswordResetView
urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',views.LoginSingUp),
    # path('singup/',views.SignUpPage, name='signup'),
    # path('login/', views.login, name='login'),
    # path('home/',views.HomePage, name='home')
    path('', views.index, name='index'),
    path('login/',views.login,name='login'),
    path('signup/', views.signup, name='signup'),
    path('forgotpass/',views.forgot_pass, name='forgot'),
    # path('reset_password/<uidb64>/<token>/', views.update_pass, name='update_pass'),
    path('reset_password/<uidb64>/<token>/', views.update_pass, name='update_pass'),
    # path('update_pass/',views.update_pass, name='update_pass'),
    path('sendmsg/',views.msg,name='msg_reset'),
    path("resetreturnhome/",views.resetreturnhome,name="resetreturnhome"),
    path("postadd/",views.post_add,name="post_add"),
    path("succes_post/",views.succes_post,name='success_post'),
    path("all_category/",views.category_prodect,name='category')
]