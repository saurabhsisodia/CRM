from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
	name=models.CharField(max_length=200,null=True)
	phone=models.CharField(max_length=200,null=True)
	email=models.EmailField(null=True)
	profile_pic=models.ImageField(default='4.jpg',null=True,blank=True)
	date_created=models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return self.name or ''

class Tag(models.Model):
	name=models.CharField(max_length=200,null=True)

	def __str__(self):
		return self.name or ''

class Product(models.Model):
	CATEGORY=(
		('Indoor','Indoor'),
		('Out Door','Out Door'),
		)
	name=models.CharField(max_length=200,null=True)
	price=models.FloatField(null=True)
	category=models.CharField(max_length=200,null=True,choices=CATEGORY)
	description=models.CharField(max_length=200,null=True,blank=True)
	date_created=models.DateTimeField(auto_now_add=True,null=True)
	tag=models.ManyToManyField(Tag)

	def __str__(self):
		return self.name or ''


class Order(models.Model):
	STATUS=(
		('Pending','Pending'),
		('Out for delivery','Out for delivery'),
		('Delivered','Delivered'),
		)

	customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
	product=models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
	date_created=models.DateTimeField(auto_now_add=True,null=True)
	status=models.CharField(max_length=200,null=True,choices=STATUS)

	def __str__(self):
		return self.product.name or ''