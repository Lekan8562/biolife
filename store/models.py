from django.db import models
from django.contrib.auth.models import  User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200,null=False)
    slug = models.SlugField(max_length=200,null=False)
    image = models.ImageField(upload_to='images/',null=True, blank=True)
    class Meta:
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name




class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/',null = True, blank = True)
    image_detail = models.ManyToManyField('ProductImage',related_name='primary_for_product')
    slug = models.SlugField(max_length=200)
    description = models.TextField(default="this is a good product")
    size = models.CharField(max_length=5,null=True,blank=True)
    qty = models.IntegerField(default=1)
    stock = models.IntegerField(default=0)
    category = models.ManyToManyField(Category,related_name='products')
    details = models.TextField(default="this is a good product and it has many functionalities")
    old_price = models.DecimalField(max_digits=10,decimal_places=2)
    new_price = models.DecimalField(max_digits=10,decimal_places=2)
   
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
        
    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to = "images/")
    title = models.CharField(max_length=250)
    is_primary_image = models.BooleanField(default=False)
    def __str__(self):
        return self.title
        

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_new_total for item in orderitems])
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
    def __str__(self):
        return str(self.pk)

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=1,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_new_total(self):
        total = self.product.new_price * self.quantity
        return total
    
    @property
    def get_old_total(self):
        total = self.product.old_price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address = models.CharField(max_length=200,null=False)
    city = models.CharField(max_length=200,null=False)
    state = models.CharField(max_length=200,null=False)
    country = models.CharField(max_length=200,null=False)
    zipcode = models.CharField(max_length=200,null=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address
    