from django.db import models
from django.contrib.auth.models import User
# Create your models here.

STATE_CHOICES=(
    ('MSA','MOMBASA'),
    ('NRB','NAIROBI'),
    ('BSA','BUSIA'),
    ('NKR','NAKURU'),
    ('BGM','BUNGOMA'),
    ('KMG','KAKAMEGA'),
    ('ELD','ELDORET'),
    ('TRK','TURKANA'),
    ('KBU','KIAMBU'),
    ('KTI','KITUI'),
)



CATEGORY_CHOICES=(
    ('CR','Curd'),
    ('ML','Milk'),
    ('LS','Lassi'),
    ('MS','Milkshake'),
    ('PN','Paneer'),
    ('GH','Ghee'),
    ('CZ','Cheese'),
    ('IC','Ice-Cream'),

)

ORDER_STATE_CHOICES=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)




class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    composition=models.TextField(default='')
    prodapp=models.TextField(default='')
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    Product_image=models.ImageField(upload_to='Product_images/')
    subcategory=models.CharField(max_length=255,default='default_value')
 



class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    locality=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField(default=0)
    state=models.CharField(choices=STATE_CHOICES,max_length=100)
   

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)   # user added to the database table
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    @property   # property for finding the total price
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    


class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.FloatField()
    razorpay_order_id=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status=models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=100,blank=True,null=True)
    paid=models.BooleanField(default=False)



class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)  # Set a default product ID
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATE_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
class wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    locality = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField(default=0)
    state = models.CharField(choices=STATE_CHOICES, max_length=100)


class Address(models.Model):
    Address = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    locality = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField(default=0)
    state = models.CharField(choices=STATE_CHOICES, max_length=100)