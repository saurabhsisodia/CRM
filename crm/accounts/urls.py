from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



app_name="accounts"
urlpatterns=[
	path('',views.home,name="home"),
	path('customer/<str:pk_test>/',views.customer,name="customer"),
	path('products/',views.products,name="products"),
	path('createorder',views.createorder,name="createorder"),
	path('updateorder/<str:pk>/',views.updateorder,name="updateorder"),
	path('deleteorder/<str:pk>/',views.deleteorder,name="deleteorder"),
	path('registerPage/',views.registerPage,name="registerPage"),
	path('LoginPage/',views.LoginPage,name="LoginPage"),
	path('logoutpage/',views.logoutpage,name="logoutpage"),
	path('userPage/',views.userPage,name="userPage"),
	path('accountsSettings/',views.accountsSettings,name="accountsSettings"),

	path('reset_password/',
		auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     	name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     	auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     	name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),


]


'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''