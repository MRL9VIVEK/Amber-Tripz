from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from home.models import Categories, Course, Level, Video, UserCourse, Payment, Questions, Test, Paper
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from.forms import ExamChoiceFrm, AnsChoice
from django.core import serializers
from macn.settings import *
import razorpay
from time import time

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))



# Create your views here.
def home(request): 
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    
    print(course)
    context = {
        'category': category,
        'course': course,
        
    }
    return render(request, 'main/home.html', context)

def contact(request):
    category = Categories.get_all_category(Categories)
    
    context = {
        'category' : category,
    }
    return render(request, 'main/contact.html', context)

def about(request): 
    category = Categories.get_all_category(Categories)
    context = {
        'category' : category,
    }
    return render(request, 'main/about.html', context)


def single_course(request): 
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    FreeCourse_count = Course.objects.filter(price = 0).count()
    PaidCourse_count = Course.objects.filter(price__gte=1).count()
    context = {
        'category' : category,
        'level' : level,
        'course' : course,
        'FreeCourse_count' : FreeCourse_count,
        'PaidCourse_count' : PaidCourse_count,
    }
    return render(request, 'main/single_course.html', context)


def filter_data(request):
    category = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    print(price)

    if price == ['PriceFree']:
       course = Course.objects.filter(price=0)
    elif price == ['PricePaid']:
       course = Course.objects.filter(price__gte=1)
    elif price == ['PriceAll']:
       course = Course.objects.all()


    elif category:
       course = Course.objects.filter(category__id__in=category).order_by('-id')

    elif level:
       course = Course.objects.filter(level__id__in = level).order_by('-id')
       
    else:
       course = Course.objects.all().order_by('-id')

    context = {
            'course' : course,
    }
    t = render_to_string('ajax/course.html', context)

    return JsonResponse({'data': t})


def SEARCH_COURSE(request):
    category = Categories.get_all_category(Categories)
    
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query)
    print(course)
    context = {
        'course':course,
        'category' : category,
    }
    return render(request,'search/search.html',context)

def COURSE_DETAILS(request, slug):
    course = Course.objects.all()
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))
    course_id = Course.objects.get(slug = slug)
    try:
        check_enroll = UserCourse.objects.get(user = request.user, course = course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None
    course = Course.objects.filter(slug = slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    context ={
        'course' : course,
        'category' : category,
        'time_duration' : time_duration,
        'check_enroll' : check_enroll,
    }
    return render(request, 'course/course_details.html', context)
    

def PAGE_NOT_FOUND(request):
    category = Categories.get_all_category(Categories)
    context = {
    'category' : category,
    }
    return render(request, "error/404.html", context)


def CHECKOUT(request, slug):
    course = Course.objects.get(slug = slug)
    action = request.GET.get('action')
    order = None

    if course.price == 0:
        course = UserCourse(
            user = request.user,
            course = course,
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

def MY_COURSE(request):
    course = UserCourse.objects.filter(user = request.user)
    context = {
        'course': course,
    }
    return render(request,'course/my-course.html', context)


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
        usercourse = UserCourse (
                user = payment.user,
                course = payment.course,
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



        # data = request.POST
        # print(data)
        # try:
            # client.utility.verify_payment_signature(data)
            # razorpay_order_id = data('razorpay_order_id')
            # razorpay_payment_id = data('razorpay_order_id')
            # payment_id = request.post.get('razorpay_payment_id', '')
            # razorpay_order_id = request.post.get('razorpay_order_id', '')
            # signature = request.post.get('razorpay_signature', '')
            # param ={
                # 'razorpay_order_id' : razorpay_order_id,
                # 'razorpay_payment_id' : payment_id,
                # 'razorpay_signature' : signature,
            # }
            # try:
                # payment = Payment.objects.get(razorpay_order_id = order_id )
            # except:
                # return HttpResponse("404 Not Found")
            # payment.razorpay_payment_id = payment_id
            # payment.status = True
            # usercourse = UserCourse (
                # user = payment.user,
                # course = payment.course,
            # )
            # usercourse.save()
            # payment.user_course = usercourse
            # payment.save()
            # client.utility.verify_payment_signature(param)
            
            # context =  {
                # 'data' : data,
                # 'payment' : payment,
                # 'param' : param,
            # }
            # return render(request, 'verify_payment/success.html', context)
        # except:
            # return render(request, 'verify_payment/fail.html')

            
def WATCH_COURSE(request, slug):
    return render(request, 'course/watch_course.html')


def TEST_SERIES(request):
    if request.method=='POST':
        form=ExamChoiceFrm(request.POST or None)
        if form.is_valid():
            # course=Course.objects.filter(course=form.cleaned_data.get('course'))[0]
            # print(course)
            test=Test.objects.filter(test=form.cleaned_data.get('test'))[0]
            request.session['test']=test.id
            paper=Paper.objects.filter(paper=form.cleaned_data.get('paper'))[0]
            request.session['paper']=paper.id
            qs = Questions.objects.filter(test=test, paper=paper)
            context ={
                'questions': qs,
                'qs': qs[0],
            }
            return render(request, 'profile/question.html', context)
    form=ExamChoiceFrm()
    context={
        'form': form,
    }
    return render(request, 'profile/test_series.html', context)

def MY_PROFILE(request):
    return render(request, 'profile/my_profile.html')



def exam_home(request, qno):
    print(qno)
    paper=request.session['paper']
    test=request.session['test']
    qts= Questions.objects.filter(test=test, paper=paper)
    qs=Questions.objects.filter(qs_no=qno)[0]
    ansfrm= AnsChoice()
    context ={
        'ansfrm': ansfrm,
        'questions': qts,
        'qs': qs,
    }
    return render(request, 'profile/question.html', context)

