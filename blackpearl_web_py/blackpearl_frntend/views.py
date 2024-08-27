from django.shortcuts import render, get_object_or_404, redirect
from blackpearl_admin.models import *
from django.db.models import Q
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from .custom_contex import customContext
from django.urls import reverse

# Create your views here.


def Userindex(request):
    context = customContext(request)
    context['category_list'] = Category.objects.all()
    context['product_list'] = Product.objects.filter(status='Active', trendy=True)
    return render(request,'index.html', context)

def getTotalValuesOfaProduct(product):
    diffVarientsOfProduct = [i for i in product.product_varients_set.all()]
    valueList = []
    for singleVarient in diffVarientsOfProduct:
        valueList.extend([i.uid for i in singleVarient.varient_values.all()])
    return list(set(valueList))

def getSelectedSizeHasColors(product,selectedSize):
    selectedSizeHasColors = []
    for item in [i for i in product.product_varients_set.filter(Varient_Values = selectedSize)]:
        selectedSizeHasColors.extend([i.id for i in item.varient_values.all() if i.Varient_Type.Varient_Name == 'Color'])
    return list(set(selectedSizeHasColors))

def getSelectedColorHasSize(product,selectedColor):
    selectedColorHasSize = []
    for item in [i for i in product.product_varients_set.filter(Varient_Values = selectedColor)]:
        selectedColorHasSize.extend([i.id for i in item.Varient_Values.all() if i.Varient_Type.Varient_Name == 'Size'])
    return list(set(selectedColorHasSize))

def CustomerLog_register(request, activity):
    user_id = request.session.get('CustomerLoginId')
    if user_id:
        try:
            user = CustomerUser.objects.get(id=user_id).username
        except:
            user = "UnknownUser"
    else:
        user = "AnonymousUser"

    log_entry = CustomerLog(user=user, activity=activity)
    log_entry.save()

def CustomerSignup(request):

    context = customContext(request)

    if 'CustomerLoginId' in request.session:
        return redirect('Userindex')

    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            request.session['CustomerLoginId'] = user.id
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'redirectUrl': '/Userindex/'})
            else:
                return redirect('Userindex')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors = form.errors.as_json()
                print(errors,'......')
                return JsonResponse({'errors': errors})
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomSignupForm()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'form': render_to_string('signup.html', {'form': form}, request=request)})
    
    return render(request, 'signup.html', {'form': form})


def CustomerSignin(request):
    context = customContext(request)

    if request.method == "POST":
        form = CustomSigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            print(email,password)
            try:
                user = CustomerUser.objects.get(email=email)
                if user.check_password(password):
                    login(request, user)
                    request.session['CustomerLoginId'] = user.id
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                        return JsonResponse({'message': 'Successfully logged in!', 'redirectUrl': reverse('Userindex')})
                    else:
                        messages.success(request, "Successfully logged in!")
                        return redirect('Userindex')
                else:
                    messages.error(request, 'Invalid email or password')
            except CustomerUser.DoesNotExist:
                messages.error(request, 'Invalid email or password')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                print(form.errors,'errorrsss......')
                return JsonResponse({'errors': form.errors}, status=400)
            else:
                messages.error(request, 'Please correct the errors below.')

    else:
        form = CustomSigninForm()

    return render(request,'signin.html', {"form":form})


def CustomerLogout(request):
    try:
        CustomerLog_register(request, 'Logout')
        if 'CustomerLoginId' in request.session:
            del request.session['CustomerLoginId']
        
        return redirect(request.META.get('HTTP_REFERER', 'Userindex'))
    except:
        return redirect('Userindex')
    

def product_list(request):
    product_list = Product_Varients.objects.all()
    return render(request,'products.html', locals())

def product_detail(request):
    Pro_id = request.GET.get('p_id')
    Itemfromurl = request.GET.get('item')
    size = request.GET.get('size')
    color = request.GET.get('color')

    context = {}
    
    product = get_object_or_404(Product, slug=Pro_id) if Pro_id else get_object_or_404(Product, id=Pro_id)

    item = product.product_varients_set.first()
    print(item,'uguggjru')

    if Itemfromurl:
            item = product.product_varients_set.filter(Q(uid = Itemfromurl) | Q(slug = Itemfromurl)).first()

    if size and color:
        item = product.product_varients_set.filter(Q(varient_values = size) & Q(varient_values = color)).first()
        if item is None:
            item = product.product_varients_set.filter(Q(varient_values = size) | Q(varient_values = color)).first()
    elif size:
        item = product.product_varients_set.filter(varient_values = size).first()
    elif color:
        item = product.product_varients_set.filter(varient_values = color).first()
    print(item,'asdfg')
    
    context['product'] = product
    context['item'] = item
    context['ProductHasTheseValues'] = getTotalValuesOfaProduct(product)
    return render(request,'product_detail.html', context)

def contact(request):
    return render(request,'contact.html')

def cart_page(request):
    return render(request,'cart.html')

def checkout_page(request):
    return render(request,'checkout.html')

