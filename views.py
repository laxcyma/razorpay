from django.shortcuts import render
import razorpay
from .models import razorpayment
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Create your views here.

# rzp_test_5DStG6Sxae0ne1
# u4JHpApEYW8GmFK59PZdDWKs
def payment_panel(request):
    if request.method == "POST":
        name = request.POST.get('name','')
        payamt = int(request.POST.get('payamt','')) * 100        
        client = razorpay.Client(auth=('rzp_test_5QkTsF3niAwffV','xF80OdawVjiIU3IJwgEzuEn8'))
        response_payment = client.order.create(dict(amount=payamt,currency='INR'))
        
        order_id = response_payment['id']
        order_status = response_payment['status']
        if order_status == 'created':
            payrazor = razorpayment(name=name,amount=payamt,order_id=order_id)
            payrazor.save()
            response_payment['name'] = name
            print(response_payment)
            context = {
                'payment':response_payment,
                'key_id':'rzp_test_5QkTsF3niAwffV'

            }
            return render(request, 'index1.html', context)
    # Create a Razorpay Order
    return render(request, 'index1.html')
    
# example =  {'id': 'order_Mjd5DMLJlcw7GZ', 'entity': 'order', 'amount': 10000, 'amount_paid': 0, 'amount_due': 10000, 'currency': 'INR', 'receipt': None, 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1696313248}

@csrf_exempt
def payment_status(request):
    if request.method == 'POST':
        response = request.POST
        print(response)
        params_dict = {
            'razorpay_order_id': response.get('razorpay_order_id'),
            'razorpay_payment_id': response.get('razorpay_payment_id'),
            'razorpay_signature': response.get('razorpay_signature')
        }

        client = razorpay.Client(auth=('rzp_test_5QkTsF3niAwffV', 'xF80OdawVjiIU3IJwgEzuEn8'))

        try:
            status = client.utility.verify_payment_signature(params_dict)
            if status:
                payrazor = razorpayment.objects.get(order_id=response.get('razorpay_order_id'))
                payrazor.razorpay_payment_id = response.get('razorpay_payment_id')
                payrazor.paid = True
                payrazor.save()
                return render(request, 'paymentsuccess.html')
            else:
                return render(request, 'paymentfail.html')
        except Exception as e:
            print(str(e))
            return render(request, 'paymentfail.html')
    else:
        return HttpResponse("Invalid request method")
