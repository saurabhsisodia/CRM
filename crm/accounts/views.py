from django.shortcuts import render,redirect,reverse
from .models import *
from .forms import OrderForm,CreateUserForm,LoginForm,CustomerForm
from django.http import HttpResponseRedirect,HttpResponse
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only

# Create your views here.
@ unauthenticated_user
def registerPage(request):
	form=CreateUserForm()
	if request.method=="POST":
		form=CreateUserForm(request.POST)
		if form.is_valid():

			' the registered user will automatically be assigned in customer group'
			user=form.save()
			group=Group.objects.get(name='customer')

			user.groups.add(group)

			' assign new user to a customer' 
			Customer.objects.create(user=user)


			return redirect(reverse('accounts:LoginPage'))

	context={'form':form}

	return render(request,'accounts/register.html',context)
@ unauthenticated_user
def LoginPage(request):
	
	form=LoginForm()
	if request.method=="POST":
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect(reverse('accounts:home'))
		else:
			messages.info(request,"user is not authenticated")
	context={'form':form}
	return render(request,'accounts/login.html',context)

def logoutpage(request):
	logout(request)
	return redirect(reverse('accounts:LoginPage'))

@ login_required(login_url='accounts:LoginPage')
@ allowed_users(allowed_roles=['customer'])
def userPage(request):

	orders=request.user.customer.order_set.all()
	total_orders=orders.count()
	delivered=orders.filter(status='Delivered').count()
	pending=orders.filter(status='Pending').count()
	context={'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}

	return render(request,'accounts/user.html',context)


@login_required(login_url='accounts:LoginPage')
@ allowed_users(allowed_roles=['customer'])
def accountsSettings(request):
	customer=request.user.customer
	form=CustomerForm(instance=customer)

	if request.method=="POST":
		form=CustomerForm(request.POST,request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context={'form':form}
	return render(request,'accounts/accounts_settings.html',context)



@ login_required(login_url='accounts:LoginPage')
@ admin_only
def home(request):

	orders=Order.objects.all()
	customers=Customer.objects.all()
	total_customers=customers.count()
	total_orders=orders.count()
	delivered=orders.filter(status='Delivered').count()
	pending=orders.filter(status='Pending').count()

	context={
		'orders':orders,
		'customers':customers,
		'total_customers':total_customers,
		'total_orders':total_orders,
		'delivered':delivered,
		'pending':pending,
	}

	return render(request,'accounts/dashboard.html',context)

@ login_required(login_url='accounts:LoginPage')
@ allowed_users(allowed_roles=['admin'])
def customer(request,pk_test):
	customer=Customer.objects.get(id=pk_test)
	orders=customer.order_set.all()

	order_count=orders.count()
	myfilter=OrderFilter(request.GET,queryset=orders)
	orders=myfilter.qs



	context={'myfilter':myfilter,'order_count':order_count,'customer':customer,'orders':orders}

	return render(request,'accounts/customer.html',context)

@ login_required(login_url='accounts:LoginPage')
@ allowed_users(allowed_roles=['admin'])
def products(request):
	products=Product.objects.all()
	return render(request,'accounts/products.html',{'products':products})
	
@ login_required(login_url='accounts:LoginPage')
@ allowed_users(allowed_roles=['admin'])
def createorder(request):

	form=OrderForm()
	if request.method=="POST":
		form=OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('accounts:home'))


	context={'form':form}
	return render(request,'accounts/order_form.html',context)

@ login_required(login_url='accounts:LoginPage')
@ allowed_users(allowed_roles=['admin'])
def updateorder(request,pk):
	order=Order.objects.get(id=pk)
	form=OrderForm(instance=order)
	if request.method=="POST":
		form=OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
			return redirect(reverse('accounts:home'))

	context={'form':form}
	return render(request,'accounts/order_form.html',context)

@ login_required(login_url='accounts:LoginPage')
@ allowed_users(allowed_roles=['admin'])
def deleteorder(request,pk):

	order=Order.objects.get(id=pk)
	if request.method=="POST":
		order.delete()
		return redirect(reverse('accounts:home'))
	context={'item':order}
	return render(request,'accounts/delete.html',context)

