from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from home.models import Categories, Course, UserCourse
from payment.models import Payment
from django.template.loader import render_to_string
from django.http import JsonResponse
import json
from json import dumps
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
# from.forms import ExamChoiceFrm, AnsChoice, AnsnChoice
from django.core import serializers
from django.http import JsonResponse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from macn.settings import *
import pandas as pd
import numpy as np
import razorpay
from time import time
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))


def CHECKOUT(request, slug):
    course = Course.objects.get(slug = slug)
    action = request.GET.get('action')
    order = None
    now = datetime.now()
    print("now = ", now)

    if course.price == 0:
        current_date = datetime.today()
        print('Current Date: ', current_date)
        print(course.validity)
        n = int(course.validity)
        future_date = current_date + relativedelta(months=n)
        print('Date - 12 months from current date: ', future_date)
        print('Date - 12 months from current date: ', future_date.date())
        print('Date - 12 months from current date: ', future_date.time())
        course = UserCourse(
            user = request.user,
            course = course,
            expiry_date = future_date
        )
        course.save()
        messages.success(request,'Course Are Successfully Enrolled')
        return redirect('my_course')

    elif action == 'create_payment':
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            country = request.POST.get('country')
            address_1 = request.POST.get('address_1')
            address_2 = request.POST.get('address_2')
            city = request.POST.get('city')
            state = request.POST.get('state')
            postcode = request.POST.get('postcode')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            order_comments = request.POST.get('order_comments')

            
            amount = (course.price * 100)
            currency = "INR"
            notes = {
                "name" : f'{first_name} {last_name} ',
                "country" : country,
                "address" : f'{address_1} {address_2}',
                "city" : city,
                "state" : state,
                "postcode" : postcode,
                "phone" : phone,
                "email" : email,
                "order_comments" : order_comments,
            }
            receipt = f"ambertripz-{int(time())}"
            order = client.order.create(
                {
                'receipt' : receipt,
                'notes' : notes,
                'amount' : amount,
                'currency' : currency,
                }
            )
            payment = Payment(
                course=course,
                user=request.user,
                order_id=order.get('id')
                
            )
            payment.save()

    context = {
            'course' : course,
            'order' : order,
        }
 
    return render(request, 'checkout/checkout.html', context)




@csrf_exempt
def VERIFY_PAYMENT(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)
    
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        payment = Payment.objects.get(order_id=provider_order_id)
        payment.payment_id = payment_id
        payment.signature_id = signature_id
        payment.status = True
        category = Categories.get_all_category(Categories)
        print(payment.course.validity)
        current_date = datetime.today()
        print('Current Date: ', current_date)
        n = int(payment.course.validity)
        future_date = current_date + relativedelta(months=n)
        print('Date - 12 months from current date: ', future_date)
        print('Date - 12 months from current date: ', future_date.date())
        print('Date - 12 months from current date: ', future_date.time())
        usercourse = UserCourse (
                user = payment.user,
                course = payment.course,
                expiry_date = future_date,
            )
        usercourse.save()
        payment.user_course = usercourse
        payment.save()
        context =  {
                'payment' : payment,
            }
        return render(request, 'verify_payment/success.html', context)
    else:
        return render(request, 'verify_payment/fail.html')