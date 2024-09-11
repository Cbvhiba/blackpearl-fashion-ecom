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
from decimal import Decimal
from django.db.models import Sum
from .my_variables import *
from django.core.paginator import Paginator

# Create your views here.
CARTADD = 10

FILTER_PRICE_RANGE = {
    '1':{'min': 0, 'max': 500},
    '2':{'min':500,'max':1000},
    '3':{'min':1000,'max':1500},
    '4':{'min':1500,'max':2000},
    '5':{'min': 2000, 'max': 2500},
    '5':{'min': 2500, 'max': 3000},
    '5':{'min': 3000, 'max': 3500},
    '5':{'min': 3500, 'max': 4000},
    '5':{'min': 4000, 'max': 4500},
    '5':{'min': 4500, 'max': 5000},
}

def Userindex(request):
    context = customContext(request)
    context['category_list'] = Category.objects.all()
    context['product_list'] = Product.objects.filter(status='Active', trendy=True)
    return render(request,'index.html', context)

def removeDuplicatesWithPaginator(queryset,page,offset):
    queryList = []
    for i in queryset:
        if i not in queryList:
            queryList.append(i)
    
    return Paginator(queryList,offset).get_page(page)

def countWithoutDuplicate(queryset):
    queryList = []
    for i in queryset:
        if i not in queryList:
            queryList.append(i)
    
    return len(queryList)

def getFirtsList(allProduct,sort_by):
    return [i.product_varients_set.order_by(sort_by).first().uid for i in allProduct if i.product_varients_set.order_by(sort_by).first() is not None]

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
    context = customContext(request)
    all_products  = Product.objects.filter(status='Active')
    product_ids  = [i.uid for i in all_products]
    variants  = Product_Varients.objects.filter(product__uid__in = product_ids )
    item_list = None
    # whishList = []

    price = request.GET.get('price')
    values = request.GET.getlist('values')
    brand_id = request.GET.get('brand')
    # Filter out any empty values
    values = [value for value in values if value]
    print(values,'...................')
    sort_by = int(request.GET.get('sort_by', 0))

    if sort_by > 4:
        sort_by = 0

    if brand_id:
        variants  = variants .filter(product__Product_Brand__uid = brand_id).distinct()
        item_list = [i.uid for i in variants]
        all_products = all_products.filter(product_varients__uid__in = item_list)

    if values:

        valid_uuids = [value for value in values if value]
        color_uuids = []
        size_uuids = []

        for uid in valid_uuids:
            try:
                variant = Varient_Values.objects.get(uid=uid)
                if variant.Varient_Type.Varient_Name == 'color':
                    color_uuids.append(uid)
                elif variant.Varient_Type.Varient_Name == 'size':
                    size_uuids.append(uid)
            except Varient_Values.DoesNotExist:
                continue  # Skip invalid UUIDs

        # color_uuids = [i for i in values if Varient_Values.objects.filter(uid = values).first().Varient_Type.Varient_Name == 'color']
        # size_uuids = [i for i in values if Varient_Values.objects.filter(uid = values).first().Varient_Type.Varient_Name == 'size']

        if color_uuids and size_uuids :
            variants  = variants .filter(varient_values__uid__in = color_uuids).filter(varient_values__uid__in = size_uuids).distinct()
    
        if color_uuids:
            variants  = variants .filter(varient_values__uid__in = color_uuids).distinct()
            
        if size_uuids :
            variants  = variants .filter(varient_values__uid__in = size_uuids).distinct()
            
        item_list = [i.uid for i in variants]
        all_products = all_products.filter(product_varients__uid__in = item_list)

    if price:
        price_range = FILTER_PRICE_RANGE.get(price, {'min': 0, 'max': float('inf')})
        min_range = price_range['min']
        max_range = price_range['max']
        all_products = all_products.filter(product_varients__display_prize__range=(min_range, max_range))
        variants = variants.filter(display_prize__range=(min_range, max_range))
        item_list = [variant.uid for variant in variants]

    all_products = all_products.order_by(SORTBY_PRODUCT.get(sort_by, 'uid')) 
    print(all_products, item_list, variants,'showw')
    context['Product'] = removeDuplicatesWithPaginator(all_products,request.GET.get('page',1),12)
    context['count'] = countWithoutDuplicate(all_products)
    context['firstList'] = getFirtsList(all_products, SORTBY_ITEM.get(sort_by, 'id'))
    context['itemlist'] = item_list
    context['item'] = variants
    context['sort_by'] = sort_by
    context['price_range'] = FILTER_PRICE_RANGE
    context['fltr_price'] = price
    context['fltr_values'] = [value for value in values if value]
    context['Vartypes'] = Varient_Type.objects.filter(status = 'Active').order_by('-uid')
    context['brands'] = Brand.objects.filter(status='Active').order_by('-uid')

    return render(request,'products.html', context)

def product_detail(request):
    Pro_id = request.GET.get('p_id')
    Itemfromurl = request.GET.get('item')
    size = request.GET.get('size')
    color = request.GET.get('color')

    context = customContext(request)
    
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
    context = customContext(request)
    return render(request,'contact.html', context)

def my_cart(request):
    context = customContext(request)
    if 'CustomerLoginId' in request.session:
        user_id = request.session.get('CustomerLoginId')
        user = get_object_or_404(CustomerUser, id = user_id)
        context['carts'] = Cart.objects.filter(user = user)
        context['maxlimit'] = CARTADD
        total_cart = TotalCart.objects.filter(user = user).first()
        context['total_cart'] = total_cart
        
    return render(request,'cart.html', context)

def add_cart(request, count):
    context = customContext(request)
    if 'CustomerLoginId' not in request.session:
        return {
            'status': 0,
            'msg': 'User not logged in'
        }
    productId = request.POST.get('item')
    print(productId)
    user = get_object_or_404(CustomerUser, id=request.session['CustomerLoginId'])
    product = get_object_or_404(Product_Varients, uid=productId)
    if product.product_stock <=0:
        return {
            'status': 'danger',
            'msg': 'Out Of Stock'
        }
    cart_item,created = Cart.objects.get_or_create(
        user = user,
        product=product,
        defaults={
            'quantity': int(count),
            'display_price': Decimal(product.display_prize) * int(count),
            'discount': (Decimal(product.display_prize) * int(count))-(Decimal(product.get_price_with_discount()) * int(count)),
            'pro_price_with_dis': Decimal(product.get_price_with_discount()) * int(count),
        }
    )

    if not created:
        # If the cart item already exists, update it
        cart_item.quantity += int(count)
        cart_item.display_price = Decimal(product.display_prize) * cart_item.quantity
        cart_item.discount = (Decimal(product.display_prize) * cart_item.quantity)-(Decimal(product.get_price_with_discount()) * cart_item.quantity)
        cart_item.pro_price_with_dis = Decimal(product.get_price_with_discount()) * cart_item.quantity
        cart_item.save()

    # Update or create the TotalCart instance
    total_cart, created = TotalCart.objects.get_or_create(user=user)
    total_cart.total_display_price =  Decimal(total_cart.total_display_price or 0) + cart_item.display_price
    total_cart.total_discount = Decimal(total_cart.total_discount or 0) + cart_item.discount
    total_cart.total_pro_price_with_dis = Decimal(total_cart.total_pro_price_with_dis or 0) + cart_item.pro_price_with_dis
    total_cart.total_quantity = Cart.objects.filter(user=user).count()
    total_cart.updated_date = timezone.now()
    total_cart.save()

    return {
        'status': 'info',
        'msg': 'Added To Cart',
        'product': product,
        'msg1': None
    }

def add_to_cart(request):
    cart_status_details = add_cart(request, 1)
    qntysts = False
    count = 0

    if cart_status_details['msg'] == "Added To Cart":
        qntysts = True
        count = Cart.objects.filter(user_id=request.session['CustomerLoginId']).count()
    
    if cart_status_details['product'] is not None:
        prod = cart_status_details['product'].uid
        data = {
            'status': cart_status_details['status'],
            'prod': prod,
            'msg': cart_status_details['msg'],
            'qntysts': qntysts,
            'count': count,
            'msg1': cart_status_details['msg1']
        }
    else:
        data = {
            'status': cart_status_details['status'],
            'prod': None,
            'msg': cart_status_details['msg'],
            'qntysts': qntysts,
            'count': count
        }

    return JsonResponse(data)


def updatecart(request):
    if 'CustomerLoginId' not in request.session:
        messages.error(request, 'User not logged in.')
        return redirect('signin')
    if request.method == 'POST':
        count = request.POST.get('count')
        cartid = request.POST.get('itemId')
            
        try:
            cart_item = Cart.objects.get(id=cartid)
        except Cart.DoesNotExist:
            messages.error(request, 'Item not found.')
            return redirect('cart')
            
        product = cart_item.product
        try:
            requested_quantity = int(count)
        except ValueError:
            messages.error(request, 'Invalid quantity.')
            return redirect('cart')

        if product.product_stock < requested_quantity or product.product_stock <=0:
            messages.warning(request,'Product is out of stock')
            return redirect('cart') 
            
        display_price = Decimal(product.display_prize)
        pro_with_discount = Decimal(product.get_price_with_discount())
        discount = Decimal(display_price - pro_with_discount)

        cart_item.quantity = requested_quantity
        cart_item.display_price = display_price * requested_quantity
        cart_item.pro_price_with_dis = pro_with_discount * requested_quantity
        cart_item.discount = discount * requested_quantity
        cart_item.save()

        user = cart_item.user
        total_display_price = user.cart_set.aggregate(total=Sum('display_price'))['total'] or Decimal('0.00')
        total_pro_price_with_dis = user.cart_set.aggregate(total=Sum('pro_price_with_dis'))['total'] or Decimal('0.00')
        total_discount = user.cart_set.aggregate(total=Sum('discount'))['total'] or Decimal('0.00')
        TotalCart.objects.update_or_create(
            user = user,
            defaults={
                'total_display_price' : total_display_price,
                'total_pro_price_with_dis' : total_pro_price_with_dis,
                'total_discount' : total_discount,
            }
                
        )
        return redirect('cart')   

    return redirect('cart')      


def remove_from_cart(request, pk):
    context = customContext(request)
    if 'CustomerLoginId' not in request.session:
        messages.error(request, 'User not logged in.')
        return redirect('signin')
    else:
        user = get_object_or_404(CustomerUser, id = request.session['CustomerLoginId'])
        print(user,'user')
        try:
            cart_item = get_object_or_404(Cart, id=pk)
            total_cart, created = TotalCart.objects.get_or_create(user=user)

            new_total_display_price = total_cart.total_display_price - cart_item.display_price
            new_total_pro_price_with_dis = total_cart.total_pro_price_with_dis - cart_item.pro_price_with_dis
            new_total_discount = total_cart.total_discount - cart_item.discount
            new_total_quantity = Cart.objects.filter(user=user).count()
            cart_item.delete()

            total_cart.total_display_price = new_total_display_price
            total_cart.total_pro_price_with_dis = new_total_pro_price_with_dis
            total_cart.total_discount = new_total_discount
            total_cart.total_quantity = new_total_quantity
            total_cart.Updated_date = timezone.now()
            total_cart.save()

            messages.info(request, f'{cart_item.product.product} removed from your cart.')
            
        except Cart.DoesNotExist:
            messages.error(request, 'The item you are trying to remove does not exist.')
        
        except total_cart.DoesNotExist:
            messages.error(request, 'Cart summary not found.')

        return redirect('cart')


def checkout_page(request):
    context = customContext(request)
    return render(request,'checkout.html', context)

