from blackpearl_frntend.models import CustomerUser

def customContext(request):
    user = None
    listOfGuestCart = None
    
    if 'CustomerLoginId' in request.session:
        user = CustomerUser.objects.get(id = request.session['CustomerLoginId'])
        
    context = {
        'customer':user
    }
    return context