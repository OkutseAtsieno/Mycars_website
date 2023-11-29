from django.contrib import admin
from .models import Product, Customer, Cart,Payment,OrderPlaced,wishlist

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'display_product_image']

    def display_product_image(self, obj):
        return obj.product_image.url if obj.product_image else ''
    display_product_image.short_description = 'Product Image'

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'display_products', 'quantity']

    def display_products(self, obj):
        return ', '.join([str(product) for product in obj.products.all()])
    display_products.short_description = 'Products'



@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display=['id','user','amount','razorpay_order_id','razorpay_payment_status','razorpay_payment_id','paid'] 


@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','ordered_date','status','payment']  
    def get_product(self, obj):
        return obj.product.title if obj.product else ''
    get_product.short_description = 'Product Title'  


@admin.register(wishlist) 
class wishlistModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product']  
