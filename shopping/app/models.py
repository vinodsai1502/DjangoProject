from django.db import models

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=False)
    phone_no = models.CharField(max_length=15, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField(null=False)
    price = models.IntegerField(null=False)
    no_of_items = models.IntegerField(null=False)
    updated_at = models.DateTimeField(auto_now=True)

class SuperUsers(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=False)
    phone_no = models.CharField(max_length=15, unique=True, null=False)
    password = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)