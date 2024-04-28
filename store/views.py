from django.shortcuts import render
from .models import *
from user.forms import UserForm,LoginForm
from django.contrib import messages
from blog.models import Post,Tag
from django.db.models import Sum
from decimal import Decimal
from django.shortcuts import get_object_or_404,redirect
from django.http import JsonResponse
import json
from django.core.paginator import Paginator

# Create your views here.


    



#MAIN VIEW
def store(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    product_list = Product.objects.filter(category__name__icontains=q)
    paginator = Paginator(product_list,12)
    page_number = request.GET.get('page', 1)
    products = paginator.page(page_number)
    categories = Category.objects.all()
    posts = Post.objects.all()
   
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items,'order':order}
    for product in products:
        old_price = Decimal(product.old_price)
        new_price = Decimal(product.new_price)
        if old_price != 0:
            product.price_cut = ((new_price-old_price)/old_price)*100
        else:
            product.price_cut = 0
    sorted_products = sorted(products, key=lambda product:product.price_cut)
    top_three_products = sorted_products[:3]
    context = {'products':products,'categories':categories,'top_three_products':top_three_products,'posts':posts,'cartItems':cartItems}
    return render(request,'home.html',context)
    

def product_detail(request,slug):
    product = get_object_or_404(Product,slug__iexact=slug)
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'product':product,'products':products,'cartItems':cartItems}
    return render(request,'store/product_detail.html',context)
    

def product_delete(request,id):
    product = get_object_or_404(OrderItem,id=id)
    product.delete()
    return redirect('cart')

def cart_delete(request):
    items = OrderItem.objects.all().delete()
    return redirect(request.META.get('HTTP_REFERER'))
    

def category_detail(request, slug):
    products_list = Product.objects.all()
    paginator = Paginator(products_list,21)
    page_number = request.GET.get('page',1)
    products = paginator.page(page_number)
    category = get_object_or_404(Category,slug__iexact = slug)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'category':category,'products':products,'cartItems':cartItems}
    return render(request,'store/category_detail.html',context)
    
    
def updateProduct(request):
    data = json.loads(request.data)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('ProductId:',productId)
    
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Product was added', safe=False)

def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':1, 'get_cart_items':0}
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)
    

def add_to_cart(request,product_id):
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if not created:
        orderItem.quantity += 1
        orderItem.save()
    return redirect(request.META.get('HTTP_REFERER'))

def increase_quantity(request,item_id):
        orderItem = get_object_or_404(OrderItem,id=item_id)
        orderItem.quantity += 1
        orderItem.save()
        return JsonResponse('Item updated successfully')
            


def update_all_quantities(request):
    if request.method == 'POST':
        for cart_item in OrderItem.objects.all():
            new_quantity = request.POST.get('quantity_' + str(cart_item.id))
            if new_quantity is not None:
                cart_item.quantity = int(new_quantity)
                cart_item.save()
    
    return redirect(request.META.get('HTTP_REFERER')) 
        


#AUTHENTICATION

def login(request):
    form = UserForm()
    context = {'form':form}
    return render(request,'registration/login.html',context)

