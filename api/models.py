from email.policy import default
from django.db import models
from django.conf import settings
import datetime
from django.forms import JSONField


User = settings.AUTH_USER_MODEL


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    title = models.CharField(max_length=120)
    author = models.TextField(default='unknown')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    summary = models.TextField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    inv = models.IntegerField(default=5)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.title

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    STATUS = (
        ('pending', 'pending'),
        ('out for delivery', 'out for delivery'),
        ('delivered', 'delivered')
    )
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, blank=True, default=STATUS[0][0], choices=STATUS)
    complete = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.customer)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property 
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def get_transaction_id():
        transaction_id = datetime.datetime.now().timestamp()
        return transaction_id

    transaction_id = models.JSONField("TransactionID", default=get_transaction_id, blank=False)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, unique=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    # @property
    # def unit_price(self):
    #     price = self.product.price 
    #     return price
    
    # unit_price = models.JSONField("UnitPrice", default=unit_price, blank=False)

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    purchase_items = models.JSONField("PurchaseItems", default=list, blank=True)
    charge_id = models.CharField(max_length=360, null=True)
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.customer)
