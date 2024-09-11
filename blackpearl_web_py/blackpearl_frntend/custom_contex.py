from blackpearl_frntend.models import CustomerUser, Cart

def customContext(request):
    user = None
    listOfCart = None
    
    if 'CustomerLoginId' in request.session:
        user = CustomerUser.objects.get(id = request.session['CustomerLoginId'])
        listOfCart = [i.product.uid for i in Cart.objects.filter(user_id = request.session['CustomerLoginId'])]
        
    context = {
        'customer':user,
        'listofcart':listOfCart,
    }
    return context