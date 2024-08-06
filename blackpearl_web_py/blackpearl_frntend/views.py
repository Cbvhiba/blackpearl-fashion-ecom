from django.shortcuts import render, get_object_or_404
from blackpearl_admin.models import *
from django.db.models import Q

# Create your views here.


def main(request):
    category_list = Category.objects.all()
    product_list = Product.objects.filter(status='Active', trendy=True)
    return render(request,'index.html', locals())

def account(request):
    return render(request,'account.html')

def getTotalValuesOfaProduct(product):
    diffVarientsOfProduct = [i for i in product.product_varients_set.all()]
    valueList = []
    for singleVarient in diffVarientsOfProduct:
        valueList.extend([i.uid for i in singleVarient.Varient_Values.all()])
    return list(set(valueList))

def getSelectedSizeHasColors(product,selectedSize):
    selectedSizeHasColors = []
    for item in [i for i in product.product_varients_set.filter(Varient_Values = selectedSize)]:
        selectedSizeHasColors.extend([i.id for i in item.Varient_Values.all() if i.Varient_Type.Varient_Name == 'Color'])
    return list(set(selectedSizeHasColors))

def getSelectedColorHasSize(product,selectedColor):
    selectedColorHasSize = []
    for item in [i for i in product.product_varients_set.filter(Varient_Values = selectedColor)]:
        selectedColorHasSize.extend([i.id for i in item.Varient_Values.all() if i.Varient_Type.Varient_Name == 'Size'])
    return list(set(selectedColorHasSize))

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
        item = product.product_varients_set.filter(Q(Varient_Values = size) & Q(Varient_Values = color)).first()
        if item is None:
            item = product.product_varients_set.filter(Q(Varient_Values = size) | Q(Varient_Values = color)).first()
    elif size:
        item = product.product_varients_set.filter(Varient_Values = size).first()
    elif color:
        item = product.product_varients_set.filter(Varient_Values = color).first()
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