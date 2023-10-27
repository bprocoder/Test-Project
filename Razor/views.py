import razorpay
from django.conf import settings
from myproject.settings import RAZORPAY_KEY_ID ,RAZORPAY_KEY_SECRET
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging

# def create_order(request):
#     if request.method == 'POST':
#         amount = int(request.POST['amount']) * 100
#         client = razorpay.Client(auth=('rzp_test_YZanJGdFBjZpu8', 'gTjQxW7dpxd49OdJSwsZXf4y'))
#         payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1'})
#         order_id = payment['id']
#         return render(request, 'payment_success.html', {'order_id':order_id})
#     else:
#         return render(request, 'payment_failure.html')


razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID , RAZORPAY_KEY_SECRET))
def create_order(request):
    order_amount = 50000
    order_currency= 'INR'
    # Rs. 200
    # currency = 'INR'
  
 
    # Create a Razorpay Order
    payment_order =razorpay_client.order.create(dict(amount=order_amount,
                                                       currency=order_currency,
                                                       payment_capture= 1))
    payment_order_id=payment_order['id']
    context={
    'amount':500 , 'api_key':RAZORPAY_KEY_ID, 'order_id':payment_order_id} 
    
 
    # order id of newly created order.
    # razorpay_order_id = razorpay_order['id']
    # callback_url = 'paymenthandler/'
 
    # # we need to pass these details to frontend.
    # context = {}
    # context['razorpay_order_id'] = razorpay_order_id
    # context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
    # context['razorpay_amount'] = amount
    # context['currency'] = currency
    # context['callback_url'] = callback_url
 
    return render(request, 'payment.html', context)
 
    



def webhook1(request):
    if request.method == 'POST':
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        data = request.POST
        try:
            client.utility.verify_payment_signature(data)
            # Payment is successful, do your processing here
        except:
            # Payment failed
            pass
        return HttpResponse(status=200)
    

# def payment_success(request):
#     return render(request, 'payment_success.html')

# def payment(request):
#     return render(request, 'payment.html')


# def payment_failure(request):
#     return render(request, 'payment_failure.html')

logger = logging.getLogger()
fh = logging.FileHandler('paymentapp_view_log.txt')
logger.addHandler(fh)
