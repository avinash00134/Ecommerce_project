from django.shortcuts import render,redirect,get_object_or_404
from . forms import SignUpForm,LoginForm,AddProductForm,EditOrderForm
from . models import Product,Category,Cart,User_Details,Order,OrderItem,SearchQuery
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
import csv
from django.template.loader import get_template
from xhtml2pdf import pisa
from taggit.models import Tag
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

# Create your views here.
# @login_required(login_url='login')
def home(request):
    carts = Cart.objects.all()
    allproducts = Product.objects.all()

    Products1 = Product.objects.filter(category=1)
    Products2 = Product.objects.filter(category=2)
    Products3 = Product.objects.filter(category=3)

    context={'Products':allproducts,'carts':carts,"Products1":Products1,"Products2":Products2,"Products3":Products3}
    return render(request,'home.html',context)

def add_to_cart(request,product_id):
    products = Product.objects.filter(id=product_id)
    carts = Cart.objects.filter(sample=product_id)
    a = None
    for i in carts:
        a = i.sample
    print(a)
    if a is None:
        for prod in products:
            if prod.stock > 0:
                form = Cart(sample=product_id,category=prod.category ,user=request.user,name=prod.name,price=prod.price,image=prod.image,quantity=1,total=prod.price)
                form.save()
    else:
        for prod in carts:
            for i in products:
                if prod.quantity < i.stock:
                    form = Cart(sample=prod.sample,category=prod.category ,user=request.user,name=prod.name,price=prod.price,image=prod.image,quantity=prod.quantity+1,total=(prod.quantity+1)*prod.price)
                    carts.delete()
                    form.save()
                else:
                    return redirect('home')
    return redirect('home')

def add_quantity(request,cart_id):
    carts = Cart.objects.filter(id=cart_id)
    for prod in carts:
        products = Product.objects.filter(id=prod.sample)
        for i in products:
            print(i.stock)
            if prod.quantity < i.stock:
                form = Cart(sample=prod.sample,category=prod.category ,user=request.user,name=prod.name,price=prod.price,image=prod.image,quantity=prod.quantity+1,total=(prod.quantity+1)*prod.price)
                carts.delete()
                form.save()
            else:
                return redirect('cart')
    return redirect('cart')

def subtract_quantity(request,cart_id):
    carts = Cart.objects.filter(id=cart_id)
    for prod in carts:
        if prod.quantity >1:
            form = Cart(sample=prod.sample,category=prod.category ,user=request.user,name=prod.name,price=prod.price,image=prod.image,quantity=prod.quantity-1,total=(prod.quantity-1)*prod.price)
            carts.delete()
            form.save()
    return redirect('cart')

def delete_product_cart(request,cart_id):
    carts = Cart.objects.filter(id=cart_id)
    carts.delete()
    return redirect('cart')

def register_customer(request):
    msg=None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_customer=True
            user.save()
            msg = "User Created"
            return redirect('home')
        else:
            msg = "form is not valid"
    else:
        form = SignUpForm()
    return render(request,'registration/registration_customer.html',{'form':form,'msg':msg})

def register_seller(request):
    msg=None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_seller=True
            user.save()
            msg = "User Created"
            return redirect('home')
        else:
            msg = "form is not valid"
    else:
        form = SignUpForm()
    return render(request,'registration/registration_seller.html',{'form':form,'msg':msg})


def login_page(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request,username=username,password=password)
            print(user)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                msg = "Invalid Credentials"
        else:
            msg = "Error Validating Form"
    return render(request,'registration/login.html',{'form':form,'msg':msg})

def logoutUser(request):
    logout(request)
    return redirect('login')

def cart(request):
    carts = Cart.objects.filter(user=request.user)
    total=0
    for i in carts:
        total+=i.total
    
    context={'Carts':carts,'total':total}
    return render(request,'cart.html',context)

def checkout(request):
    carts = Cart.objects.filter(user=request.user)
    total=0
    
    for i in carts:
        total+=i.total
    if request.method == "POST":
            user_details = User_Details.objects.filter(user=request.user,status="No")
            user_details.delete()
            fname = request.POST.get("first_name")
            lname = request.POST.get("last_name")
            address = request.POST.get("address")
            mobilenumber = request.POST.get("mobilenumber")
            email = request.POST.get("email")
            country = request.POST.get("country")
            state = request.POST.get("state")
            city = request.POST.get("city")
            pincode = request.POST.get("pincode")

            form = User_Details(user=request.user,fname=fname,lname=lname,address=address,mobilenumber=mobilenumber,email=email,
                                country=country,state=state,city=city,pincode=pincode,status="No")
            form.save()

            context={'carts':carts,'total':total,'fname':fname,'lname':lname,'address':address,'mobilenumber':mobilenumber,'email':email,'country':country,'state':state,'city':city,'pincode':pincode}    
            return render(request,'payment.html',context)
    context={'carts':carts,'total':total}
    return render(request,'checkout.html',context)

def my_orders(request):
    carts = Cart.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    
    context = {'carts':carts,'orders':orders}

    return render(request,'my_orders.html',context)

def order(request,data):
    carts = Cart.objects.filter(user=request.user)
    user_details = User_Details.objects.filter(user=request.user,status="No")
    order = Order.objects.all()
    order_id=1
    for i in order:
        order_id+=1
    total=0
    for i in carts:
        total+=i.total
    print(data)

    for i in user_details:
        order_product = Order(user=request.user,order_number="OD"+str(order_id)+str(i.mobilenumber)+str(i.pincode),first_name=i.fname,last_name=i.lname,
                              email=i.email,mobilenumber=i.mobilenumber,address=i.address,country=i.country,state=i.state,city=i.city,
                              pincode=i.pincode,order_note="You Order has Pending",order_total=total)
        order_product.save()
        order_detail = Order.objects.filter(user=request.user,order_number = "OD"+str(order_id)+str(i.mobilenumber)+str(i.pincode))
        for cart in carts:
            product_detail = Product.objects.filter(id=cart.sample)
            for product in product_detail:
                for o in order_detail:
                    order_item = OrderItem(order=o,product=product,quantity=cart.quantity,
                                        price=cart.price,total=cart.total)
                    order_item.save()

    for j in carts:
        product = Product.objects.filter(id=j.sample)
        for i in product:
            i.stock-=j.quantity
            i.save()
    carts.delete()
    # order = Order.objects.all()
    # for i in order:
    #     print(i.created_at)


    carts = Cart.objects.filter(user=request.user)
    # subject = 'Your Order From CodeMarket'
    # message="Your Order is Succesfully Done. Thank you for order from our website . I hope you visit again."
    # email_from = settings.EMAIL_HOST_USER
    # recipient_email = ['youremailid']

    # send_mail(subject,message,email_from,recipient_email)

    context={'Carts':carts}
    return render(request,'order_confirmation.html',context)

def payment(request):
    return render(request,'payment.html')

def add_product(request):
    if request.user.is_authenticated:
        form = AddProductForm()
        if request.method == "POST":
            form = AddProductForm(request.POST,request.FILES)
            if form.is_valid():
                prod = form.save(commit=False)
                prod.user = request.user
                prod.save()
                return redirect('home')
        context = {"form":form}
        return render(request,'add_product.html',context)
    else:
        return render(request,'Error_page.html')

def view_product(request):
    products = Product.objects.filter(user=request.user)
    context = {"products":products}
    return render(request,'view_product.html',context)

def edit_product(request,prod_id):
    obj = get_object_or_404(Product, id=prod_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddProductForm(request.POST or None, request.FILES,instance=obj,)
            if form.is_valid():
                prod = form.save(commit=False)
                prod.save()
                form.save_m2m()
                return redirect('home')
        form = AddProductForm(instance=obj)
        context = {"object":object,"form":form}
        return render(request,'edit_product.html',context)
    else:
        return render(request,'Error_page.html')

def delete_product(request,prod_id):
    obj = get_object_or_404(Product, id=prod_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            obj.delete()
            return redirect('home')
        context = {'object':obj}
        return render(request,'delete_product.html',context)
    else:
        return render(request,'Error_page.html')

def view_product_detail(request,prod_id,tag_slug=None):
    carts = Cart.objects.all()
    product = Product.objects.filter(id=prod_id)
    
    tags = Tag.objects.all()
    find = None
    tag=None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        similar = Product.objects.filter(tags__in=[tag]).exclude(id=prod_id)
        find = True
    else:
        for i in product:
            for j in tags:  
                similar = Product.objects.prefetch_related('tags').filter(category=i.category,tags__name__in=['tag1'])
    context={'product':product,'carts':carts,'similar':similar,'tags':tags,'find':find}
    return render(request,'view_product_details.html',context)

def products_csv(request):
    if request.user.is_authenticated:
        product_one = []
        categorys = Category.objects.filter(id=3)
        with open('/home/abhishek/Downloads/Projects/Experiment No 3/EcommerceWebsite/account/templates/Products.csv') as product_file:
            product_reader = csv.DictReader(product_file)
            for j in product_reader:
                data=j
                # print(data.values())
                for i in data.values():
                    product_one.append(i)
                print(product_one)
                for i in categorys:
                    form = Product(category=i,name=product_one[0],description=product_one[1],price=product_one[2],
                                        image=product_one[3],stock=product_one[4])
                form.user = request.user
                form.save()

                product_one = []         
                
        return redirect('view_product')
    else:
        return render(request,'Error_page.html')

def request_order(request):
    # orders_all = Order.objects.filter(status="Pending")
    orders_all = Order.objects.all()
    context = {"order_details":orders_all}
    return render(request,'request_order.html',context)

def edit_order(request,ord_id):
    obj = get_object_or_404(Order, id=ord_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            form = EditOrderForm(request.POST or None, request.FILES,instance=obj,)
            if form.is_valid():
                prod = form.save(commit=False)
                prod.save()
                return redirect('home')
        form = EditOrderForm(instance=obj)
        context = {"object":object,"form":form}
        return render(request,'edit_order.html',context)
    else:
        return render(request,'Error_page.html')
    
def delete_order(request,ord_id):
    obj = get_object_or_404(Order, id=ord_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            obj.delete()
            return redirect('home')
        context = {'object':obj}
        return render(request,'delete_order.html',context)
    else:
        return render(request,'Error_page.html')

def cancel_order(request,ord_id):
    obj = get_object_or_404(Order, id=ord_id)
    if request.user.is_authenticated:
        if request.method == "POST":
            order_item = OrderItem.objects.filter(order=ord_id)
            for i in order_item:
                product = Product.objects.filter(id=i.product.id)
                for j in product:
                    j.stock+=i.quantity
                    j.save()
            obj.delete()
            return redirect('home')
        context = {'object':obj}
        return render(request,'cancel_order.html',context)
    else:
        return render(request,'Error_page.html')
    
def view_order(request,ord_id):
    if request.user.is_authenticated:
        order = Order.objects.filter(id=ord_id)
        carts = Cart.objects.all()
        order_item = OrderItem.objects.filter(order=ord_id)
        for i in order_item:
            quantity = i.quantity
        
        
        context = {"order_item":order_item,"carts":carts,"order":order}
        return render(request,'view_order.html',context)
    else:
        return render(request,'Error_page.html')
    
def render_pdf_view(request,ord_id):
    if request.user.is_authenticated:
        template_path = 'download.html'
        order = Order.objects.filter(id=ord_id)
        carts = Cart.objects.all()
        order_item = OrderItem.objects.filter(order=ord_id)
        context = {"order_item":order_item,"carts":carts,"order":order}    # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'

        template = get_template(template_path)
        html = template.render(context)

        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        return render(request,'Error_page.html')

def search_view(request):
    query= request.GET.get('q', None)
    user = None
    if request.user.is_authenticated:
        user = request.user
    context = {"query":query}
    if query is not None:
        SearchQuery.objects.create(user=user, query=query)
        
        multiple_query = Q(Q(name__icontains=query) | Q(price__icontains = query))
        product_list = Product.objects.filter(multiple_query)
    else:
        product_list = Product.objects.all()
    context['product_list'] = product_list
    return render(request, 'search.html', context)

    