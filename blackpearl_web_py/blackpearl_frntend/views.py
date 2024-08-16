from django.shortcuts import render, get_object_or_404, redirect
from blackpearl_admin.models import *
from django.db.models import Q
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.


def Userindex(request):
    category_list = Category.objects.all()
    product_list = Product.objects.filter(status='Active', trendy=True)
    return render(request,'index.html', locals())

def CustomerSignin(request):
    return render(request,'signin.html')

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

def CustomerSignup(request):
    if 'CustomerLoginId' in request.session:
        return redirect('Userindex')

    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            # Create user instance but don't save to the database yet
            user = form.save(commit=False)
            # Hash the password before saving
            user.password = make_password(form.cleaned_data['password1'])
            user.save()
            request.session['CustomerLoginId'] = user.uid
            return redirect('Userindex')
        else:
            # Form is not valid, display errors
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomSignupForm()

    return render(request, 'signup.html', {'form': form})

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