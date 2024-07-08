from datetime import datetime
from pyexpat import model
from unicodedata import category
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group
from Auth.models import User

# Create your models here.

class Employees(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100,blank=True) 
    firstname = models.TextField() 
    middlename = models.TextField(blank=True,null= True) 
    lastname = models.TextField() 
    gender = models.TextField(blank=True,null= True) 
    dob = models.DateField(blank=True,null= True) 
    contact = models.TextField() 
    address = models.TextField() 
    email = models.TextField() 

    date_hired = models.DateField() 
    salary = models.FloatField(default=0) 
    status = models.IntegerField() 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.firstname + ' ' +self.middlename + ' '+self.lastname + ' '

class Category(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField(default=1) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    udpated_by = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Sales(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now) 
    date_invoice = models.DateTimeField(null= True) 
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE,null= True)
    updated_by = models.CharField(max_length=100)
    discount = models.FloatField(default=0)
    nameCustomer = models.TextField(default="-") 
    phoneCustomer = models.TextField(default="-") 
    statusPPN = models.TextField(default="Tidak") 
    ppn = models.TextField(null= True) 
    npwp = models.TextField(null= True)
    statusRetur = models.TextField(null= True)
    typePayment = models.TextField(null= True)

    def __str__(self):
        return self.code

class incomingGoods(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    discount = models.FloatField(default=0)

    def __str__(self):
        return self.code

class outletProudct(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True)
    date_invoice = models.DateTimeField(null= True) 
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    discount = models.FloatField(default=0)
    typePayment = models.TextField(default="kartu_stock") 

    def __str__(self):
        return self.code


class masterApps(models.Model):
    uri = models.CharField(max_length=100)
    name = models.TextField()
    description = models.TextField()
    logo = models.CharField(max_length=100)
    customize = models.TextField()
     
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class supplier(models.Model):
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField(default=1) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100)
    udpated_by = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Products(models.Model):
    code = models.CharField(max_length=100)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier_id = models.ForeignKey(supplier, on_delete=models.CASCADE, null= True)
    name = models.TextField()
    description = models.TextField()
    status = models.IntegerField(default=1) 
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    price = models.FloatField(default=0)
    selling_price = models.FloatField(default=0)
    image = models.ImageField(upload_to='images/', null= True)

    def __str__(self):
        return self.code + " - " + self.name



class incomingGoodsItems(models.Model):
    incomingGoods_id = models.ForeignKey(incomingGoods,on_delete=models.CASCADE)
    outletProduct_id = models.ForeignKey(outletProudct,on_delete=models.CASCADE, null= True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)
    serial_number = models.TextField(blank=True,null= True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE,null= True)
    statusPayment = models.TextField(default="Belum")
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
    
class salesItems(models.Model):
    sale_id = models.ForeignKey(Sales,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    serial_number = models.TextField(blank=True,null= True)
    total = models.FloatField(default=0)
    incomingGoodsItems_id = models.ForeignKey(incomingGoodsItems,on_delete=models.CASCADE, null= True)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 

class outletProudctItem(models.Model):
    incomingGoodsItems_id = models.ForeignKey(incomingGoodsItems,on_delete=models.CASCADE, null= True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)
    serial_number = models.TextField(blank=True,null= True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE,null= True)
    outletProduct_id = models.ForeignKey(outletProudct,on_delete=models.CASCADE, null= True)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True) 
    
    
class martDataSales(models.Model):
    date = models.DateTimeField(default=timezone.now)
    total = models.FloatField(default=0)
    qty = models.IntegerField(default=0)
    transact = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'mart_data_sales'
        
class tableTrans(models.Model):
    code_trans = models.CharField(max_length=100)
    user_id_trans = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'table_transisi'

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    parent_id = models.IntegerField(default=0)
    def __str__(self):
        return self.title

class bast(models.Model):
    code = models.CharField(max_length=100)
    sub_total = models.FloatField(default=0)
    grand_total = models.FloatField(default=0)
    tax_amount = models.FloatField(default=0)
    tax = models.FloatField(default=0)
    tendered_amount = models.FloatField(default=0)
    amount_change = models.FloatField(default=0)
    date_added = models.DateTimeField(default=timezone.now) 
    date_updated = models.DateTimeField(auto_now=True)
    date_invoice = models.DateTimeField(null= True) 
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    discount = models.FloatField(default=0)
    typePayment = models.TextField(default="BAST") 
    nameCustomer = models.TextField(default="-") 
    phoneCustomer = models.TextField(default="-")
    address = models.TextField(default="-")

    def __str__(self):
        return self.code

class bastItem(models.Model):
    incomingGoodsItems_id = models.ForeignKey(incomingGoodsItems,on_delete=models.CASCADE, null= True)
    product_id = models.ForeignKey(Products,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    qty = models.FloatField(default=0)
    total = models.FloatField(default=0)
    serial_number = models.TextField(blank=True,null= True)
    bast_id = models.ForeignKey(bast,on_delete=models.CASCADE, null= True)