from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate , login
from django.contrib import messages
from .models import Users , Products , SuperUsers
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    return render(request,'home.html')

def user(request):
    return render(request,'users_page.html')

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confirm password are not Same!!")
        else:
            my_user = Users.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('admin_login')

    return render(request, 'signup_page.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('success_page')
            else:
                pass
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def search_view(request):

    query = request.GET['query']
    products = Products.objects.all().filter(name__icontains=query)
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    word = "Searched Result :"

    if request.user.is_authenticated:
        return render(request,
                      {'products': products, 'word': word, 'product_count_in_cart': product_count_in_cart})
    return render(request, 'ecom/index.html',
                  {'products': products, 'word': word, 'product_count_in_cart': product_count_in_cart})


def add_to_cart_view(request, pk):
    products = Products.objects.all()

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 1

    response = render(request,
                      {'products': products, 'product_count_in_cart': product_count_in_cart})

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids == "":
            product_ids = str(pk)
        else:
            product_ids = product_ids + "|" + str(pk)
        response.set_cookie('product_ids', product_ids)
    else:
        response.set_cookie('product_ids', pk)

    product = Products.objects.get(id=pk)
    messages.info(request, product.name + ' added to cart successfully!')

    return response


def cart_view(request):
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0
    products = None
    total = 0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        if product_ids != "":
            product_id_in_cart = product_ids.split('|')
            products = Products.objects.all().filter(id__in=product_id_in_cart)

            for p in products:
                total = total + p.price
    return render(request,
                  {'products': products, 'total': total, 'product_count_in_cart': product_count_in_cart})


class LoginForm(AuthenticationForm):
    pass


def remove_from_cart_view(request, pk):
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        product_count_in_cart = len(set(counter))
    else:
        product_count_in_cart = 0

    total = 0
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        product_id_in_cart = product_ids.split('|')
        product_id_in_cart = list(set(product_id_in_cart))
        product_id_in_cart.remove(str(pk))
        products = Products.objects.all().filter(id__in=product_id_in_cart)
        for p in products:
            total = total + p.price

        value = ""
        for i in range(len(product_id_in_cart)):
            if i == 0:
                value = value + product_id_in_cart[0]
            else:
                value = value + "|" + product_id_in_cart[i]
        response = render(request,
                          {'products': products, 'total': total, 'product_count_in_cart': product_count_in_cart})
        if value == "":
            response.delete_cookie('product_ids')
        response.set_cookie('product_ids', value)
        return response
