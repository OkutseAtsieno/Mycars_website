from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from .models import Product, Customer, Cart, wishlist,OrderPlaced,Address
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required


def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(wishlist.objects.filter(user=request.user))
    return render(request, "about.html", locals())


def contact(request):
    wishitem = 0
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(wishlist.objects.filter(user=request.user))
    return render(request, "contact.html", locals())


def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(wishlist.objects.filter(user=request.user))
    return render(request, "home.html", locals())


def base(request):
    return render(request, "base.html")


class CategoryView(View):
    template_name = 'category.html'

    def get(self, request, subcategory=None):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        products = Product.objects.filter(subcategory=subcategory)
        category_title = 'val'
        title = Product.objects.filter(category=category_title).values('title')
        return render(request, self.template_name, {'products': products, 'category': title})

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist_items = wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request, "Productdetail.html", locals())





class CategoryTitleView(View):
    def get(self, request, val):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, "productdetail.html", locals())


class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist_items = wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request, "Productdetail.html", locals())


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request, 'customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User registration successful")
            return HttpResponse("User registration successful")
        else:
            messages.warning(request, "Invalid input data")
            return render(request, 'customerregistration.html', {'form': form})


class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request, 'profile.html', {'form': form})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state,
                           zipcode=zipcode)
            reg.save()

            messages.success(request, "Profile saved successfully")
            return render(request, 'profile.html', {'form': form})
        else:
            messages.warning(request, "Invalid input data")
            return render(request, 'profile.html', {'form': form})


class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        return render(request, 'updateAddress.html', locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, 'Congratulations! Profile updated successfully')
            return redirect("address")
        else:
            messages.warning(request, "Invalid input data")

        return render(request, 'updateAddress.html', {'form': form})



def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')  # product Id
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')  # add to the items table


@login_required
def address(request):
    totalitem = len(Cart.objects.filter(user=request.user))
    
    try:
        addresses = Address.objects.filter(Address__user=request.user)
    except Address.DoesNotExist:
        addresses = []

    return render(request, 'address.html', {'totalitem': totalitem, 'addresses': addresses})

def show_cart(request):
    user = request.user  # get all the cart items whre the user is the login user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + 500  # shipping fee
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'addtocart.html', locals())  # add all the cart data


from django.http import JsonResponse
from django.db.models import Q


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
            amount = 0
            cart = Cart.objects.filter(user=request.user)

            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount += value

            gst = 0.18 * amount  # gst is 18% of the total amount

            # Shipping fee
            shipping_fee = 500

            # Total amount including GST and shipping fee
            total_amount = amount + gst + shipping_fee

            data = {
                'quantity': cart_item.quantity,
                'amount': amount,
                'gst': gst,
                'shipping_fee': shipping_fee,
                'total_amount': total_amount
            }
            return JsonResponse(data)
        else:
            data = {
                'error': 'Product not found in the cart.'
            }
            return JsonResponse(data)
    else:
        data = {
            'error': 'Invalid request method.'
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()

        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()  # Remove the item from the cart if quantity becomes 0

            amount = 0
            cart = Cart.objects.filter(user=request.user)

            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount += value

            # Assuming GST is 18% of the total amount
            gst = 0.18 * amount

            # Shipping fee
            shipping_fee = 500

            # Total amount including GST and shipping fee
            total_amount = amount + gst + shipping_fee

            data = {
                'quantity': cart_item.quantity if cart_item.quantity > 0 else 0,
                'amount': amount,
                'gst': gst,
                'shipping_fee': shipping_fee,
                'total_amount': total_amount
            }
            return JsonResponse(data)
        else:
            data = {
                'error': 'Product not found in the cart.'
            }
            return JsonResponse(data)
    else:
        data = {
            'error': 'Invalid request method.'
        }
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        cart_item = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()

        if cart_item:
            cart_item.delete()  # Remove the item from the cart

            amount = 0
            cart = Cart.objects.filter(user=request.user)

            for p in cart:
                value = p.quantity * p.product.discounted_price
                amount += value

            # Assuming GST is 18% of the total amount
            gst = 0.18 * amount

            # Shipping fee
            shipping_fee = 500

            # Total amount including GST and shipping fee
            total_amount = amount + gst + shipping_fee

            data = {
                'message': 'Product removed from the cart',
                'amount': amount,
                'gst': gst,
                'shipping_fee': shipping_fee,
                'total_amount': total_amount
            }
            return JsonResponse(data)
        else:
            data = {
                'error': 'Product not found in the cart.'
            }
            return JsonResponse(data)
    else:
        data = {
            'error': 'Invalid request method.'
        }
        return JsonResponse(data)


class Checkout(View):
    def get(self, request):
        totalitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))

        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount + 500
        return render(request, 'checkout.html', locals())

    def post(self, request):
        # Implement your checkout logic here
        pass


def orders(request):
        totalitem=0
        if request.user.is_authenticated:
            totalitem=len(Cart.objects.filter(user=request.user))
            OrderPlaced.objects.filter(user=request.user)
            return render(request,'orders.html',locals())


def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        wishlist(user=user, product=product).save()
        data = {
            'message': 'Wishlist added successfully',
        }
        return JsonResponse(data)


def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        wishlist(user=user, product=product).delete()
        data = {
            'message': 'Wishlist removed successfully',
        }
        return JsonResponse(data)