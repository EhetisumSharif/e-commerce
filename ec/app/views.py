# views.py
from django.db.models import Count 
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View 
from .models import Customer, OrderPlaced, Payment, Product, Cart, Wishlist
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages 
from django.db.models import Q
from sslcommerz_lib import SSLCOMMERZ
import uuid
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/home.html', locals())

def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/about.html', locals())

def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/contact.html', locals())

class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html', locals())

class CategoryTitle(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'app/category.html', locals())
    
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = None  # Initialize wishlist to None
        if request.user.is_authenticated:
            wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', locals())

class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/customerregistration.html', locals())
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulation! User Register Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/customerregistration.html', locals())

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form})  

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city, mobile=mobile, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid input data")
        return render(request, 'app/profile.html', {'form': form})

@login_required    
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/address.html', locals())

@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/updateAddress.html', {'form': form})

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
            messages.success(request, "Address updated successfully")
        else:
            messages.warning(request, "Invalid input data")
        return redirect("address")
    
@login_required   
def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')  

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0.0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount= amount + value
    totalamount = amount + 110
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/addtocart.html', locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request, 'app/wishlist.html', locals())

# SSLCOMMERZ Settings
settings = {
    'store_id': 'testbox',
    'store_pass': 'qwerty',
    'issandbox': True
}

@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = sum(p.quantity * p.product.discounted_price for p in cart_items)
        totalamount = famount + 110
        return render(request, 'app/checkout.html', locals())

    def post(self, request):
        user = request.user
        customer_id = request.POST.get('custid')
        customer = Customer.objects.get(id=customer_id)
        
        cart_items = Cart.objects.filter(user=user)
        total_amount = sum(p.quantity * p.product.discounted_price for p in cart_items) + 110
        
        # Generate a unique transaction ID
        tran_id = "TRANS_" + str(uuid.uuid4())
        
        # Create a payment record with 'Pending' status
        payment = Payment(user=user, amount=total_amount, sslcommerz_tran_id=tran_id, sslcommerz_status='Pending')
        payment.save()
        
        # Prepare post body for SSLCOMMERZ
        sslcz = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = total_amount
        post_body['currency'] = "BDT"
        post_body['tran_id'] = tran_id
        post_body['success_url'] = request.build_absolute_uri(reverse('sslcommerz_success'))
        post_body['fail_url'] = request.build_absolute_uri(reverse('sslcommerz_fail'))
        post_body['cancel_url'] = request.build_absolute_uri(reverse('sslcommerz_cancel'))
        post_body['emi_option'] = 0
        post_body['cus_name'] = customer.name
        post_body['cus_email'] = user.email
        post_body['cus_phone'] = str(customer.mobile)
        post_body['cus_add1'] = customer.locality
        post_body['cus_city'] = customer.city
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['product_name'] = "Online Shopping"
        post_body['product_category'] = "Goods"
        post_body['product_profile'] = "general"

        response = sslcz.createSession(post_body)
        
        if 'GatewayPageURL' in response and response['GatewayPageURL']:
            return redirect(response['GatewayPageURL'])
        else:
            messages.error(request, 'Failed to connect to payment gateway.')
            return redirect('checkout')

# New Views for Handling Callbacks
@method_decorator(csrf_exempt, name='dispatch')
class SslcommerzSuccessView(View):
    def post(self, request):
        sslcz = SSLCOMMERZ(settings)
        post_body = request.POST
        if sslcz.hash_validate_ipn(post_body):
            val_id = post_body.get('val_id')
            tran_id = post_body.get('tran_id')
            response = sslcz.validationTransactionOrder(val_id)
            
            if response['status'] == 'VALID':
                payment = Payment.objects.get(sslcommerz_tran_id=tran_id)
                payment.sslcommerz_status = 'VALID'
                payment.paid = True
                payment.save()
                user = payment.user
                customer = Customer.objects.filter(user=user).first()
                cart_items = Cart.objects.filter(user=user)
                for item in cart_items:
                    OrderPlaced(user=user, customer=customer, product=item.product, quantity=item.quantity, status='Accepted', payment=payment).save()
                cart_items.delete()
                messages.success(request, 'Payment successful and order placed!')
                return redirect('orders')
            else:
                messages.error(request, 'Payment validation failed.')
                return redirect('checkout')
        else:
            messages.error(request, 'Payment validation failed.')
            return redirect('checkout')
        
@method_decorator(csrf_exempt, name='dispatch') # <-- Add this decorator
class SslcommerzFailView(View):
    def post(self, request):
        tran_id = request.POST.get('tran_id')
        payment = Payment.objects.get(sslcommerz_tran_id=tran_id)
        payment.sslcommerz_status = 'FAILED'
        payment.save()
        messages.error(request, 'Payment failed.')
        return redirect('checkout')
    
@method_decorator(csrf_exempt, name='dispatch') # <-- Add this decorator
class SslcommerzCancelView(View):
    def post(self, request):
        tran_id = request.POST.get('tran_id')
        payment = Payment.objects.get(sslcommerz_tran_id=tran_id)
        payment.sslcommerz_status = 'CANCELED'
        payment.save()
        messages.error(request, 'Payment was canceled.')
        return redirect('checkout')

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount= amount + value
        totalamount = amount + 110
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
   
@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed': order_placed})

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount= amount + value
        totalamount = amount + 110
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount= amount + value
        totalamount = amount + 110
        data = {
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)
    
@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user=request.user
        Wishlist(user=user, product=product).save()
        data={
            'message': 'Wishlist Added Successfully'
        }
        return JsonResponse(data)
    
@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Wishlist Removed Successfully'
        }
        return JsonResponse(data)
    
def search(request):
    query = request.GET.get('search', '')
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,"app/search.html", locals())