from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from home.models import Categories, Course, Level, Video, UserCourse, Payment, Questions, Test, Paper, Time, Answer, Ans, Que, Result, Contact, Ppr, Subject
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from.forms import ExamChoiceFrm, AnsChoice, AnsnChoice
from django.core import serializers
from django.http import JsonResponse
from macn.settings import *
import razorpay
from time import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

client = razorpay.Client(auth=(KEY_ID, KEY_SECRET))



# Create your views here.
def home(request): 
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    context = {
        'category': category,
        'course': course,
        
    }
    return render(request, 'main/home.html', context)

def contact(request):
    
    if request.method=="POST":
        name = request.POST.get('name')
        # print(name)
        
        emailn = request.POST.get('email')
        message = request.POST.get('message')
        contact = Contact(name=name, email=emailn, desc=message)
        # print(emailn)
        emailo= Contact.objects.filter(email=emailn)
        # print(emailo)
        if emailo:
            pass
        else:
            contact.save()
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
    print(query)
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


def MY_COURSE(request):
    course = UserCourse.objects.filter(user = request.user)
    category = Categories.get_all_category(Categories)
    
    context = {
        'course': course,
        'category' : category,
    }
    return render(request,'course/my-course.html', context)


def MY_COURSE_SLUG(request, slug):
    course = Course.objects.get(slug = slug)
    category = Categories.get_all_category(Categories)
    course_all = Course.objects.all()
    print(course)
    context = {
    'course' : course,
    'category' : category,
    'course_all': course_all,
    }
    return render(request, "profile/profile.html", context)

def MY_TEST_SERIES(request):
    course = UserCourse.objects.filter(user = request.user)
    category = Categories.get_all_category(Categories)
    
    context = {
        'course': course,
        'category' : category,
    }
    return render(request,'profile/my_test_series.html', context)


def MY_TEST_SERIES_SLUG(request, slug):
    course = Course.objects.get(slug = slug)
    category = Categories.get_all_category(Categories)
    time = Time.objects.filter(student = request.user, course = course)
    context = {
    'course' : course,
    'category' : category,
    'time' : time,
    }
    return render(request, "profile/online_test.html", context)

def instructions(request, slug):
    ppr = Ppr.objects.get(new_slug = slug)
    subject = Subject.objects.filter(course = ppr.course) 
    time = Time.objects.filter(student = request.user, course = ppr.course, ppr = ppr)
    if time :
        pass
        
    else:
        time = Time(student = request.user, course = ppr.course, ppr = ppr, time = ppr.time_duration)
        time.save()
    context = {
        'ppr' : ppr,
        'time' : time,
        'subject' : subject,
    }
    return render(request, "test/instructions.html", context)

def Question(request, slug):
    ppr = Ppr.objects.get(new_slug = slug)
    # print(ppr)
    subject = Subject.objects.filter(course = ppr.course)
    # print(subject)
    que = Que.objects.filter(course = ppr.course, ppr = ppr)
    # print(que)
    q = Que.objects.filter(course = ppr.course, ppr = ppr)
    paginator=Paginator(que, 1)
    page_number = request.GET.get('page', 1)
    que = paginator.get_page(page_number)
    ansnfrm=AnsnChoice()
    if request.method=="POST":
        ansn = request.POST.get('ansn')
        
        quen = Que.objects.get(course = ppr.course, ppr = ppr, qs_no = page_number)
        
        if ansn == quen.answers:
            s=1
        elif ansn != quen.answers:
            s= -1
        else :
            s=0
        
        ans = Ans(student=request.user, course = ppr.course, ppr=ppr, que_no = quen.qs_no, que = quen, answer=ansn, correct_answer = quen.answers, score=s)
        ans.save()
    context = {
        'subject' : subject,
        'ppr' : ppr,
        'que' : que,
        'ansnfrm' : ansnfrm,
        'q' : q,
    }
    return render(request, "test/question.html", context)

def number_que(request):

    if request.method == 'POST':
        sid = request.POST['sid']
        print(sid)
        ppr = request.POST['ppr']
        print(ppr)
        ppr = Ppr.objects.get(title = ppr)
        print(ppr.title)
        print(ppr.course)
        que = Que.objects.get(course = ppr.course, ppr = ppr, qs_no = sid)
        print(que)
        quen = {"qs_no" : que.qs_no, "questions" : que.questions, "option_a" : que.option_a, "option_b" : que.option_b, "option_c" : que.option_c, "option_d" : que.option_d}
        ansnfrm=AnsnChoice()
        print(ansnfrm)
        ans = list(ansnfrm)
        print(ans)
        # que = Que.objects.values().filter(course = ppr.course, ppr = ppr, qs_no = sid)
        # que_n = list(que)
        # print(que_n)
        return JsonResponse(quen)
    else:
        return JsonResponse({'status': 0})
        
        # que_detail = {"qs_no": que.qs_no, "course": que.course, "ppr": que.ppr, "questions": que.questions, "answers":que.answers, "option_a": que.option_a, "option_b": que.option_b, "option_c": que.option_c, "option_d": que.option_d, "disc": que.disc}
        # return JsonResponse(que_detail)


def next_que(request):
    if request.method == 'POST':
        sid = request.POST['sid']
        ppr = request.POST['ppr']
        que_n = request.POST['que']
        opt_v = request.POST['ans']
        # print(que_n)
        # print(opt_v)
        ppr = Ppr.objects.get(title = ppr)
        que_a =Que.objects.get(course = ppr.course, ppr = ppr, qs_no = que_n)
        # print(que_a.answers)
        # print(que_a)
        getqs=Ans.objects.filter(student=request.user, course = ppr.course, ppr=ppr, que_no=que_n).delete()
        ans = Ans(student=request.user, course = ppr.course, ppr=ppr, que_no=que_n, que=que_a, answer=opt_v, correct_answer=que_a.answers, score=1)
        ans.save()
        que_count = Que.objects.filter(course = ppr.course, ppr = ppr).count()
        id = int(sid)
        if id <= que_count :
            sid = id
        else:
            sid = 1
        # print(ppr.course)
        que = Que.objects.get(course = ppr.course, ppr = ppr, qs_no = sid)
        # answer = Ans.objects.filter(student=request.user, course = ppr.course, ppr=ppr, que_no=sid)
        # print(answer)
        # print(que)
        quen = {"qs_no" : que.qs_no, "questions" : que.questions, "option_a" : que.option_a, "option_b" : que.option_b, "option_c" : que.option_c, "option_d" : que.option_d}
        # answer_n = {"answer": answer}
        return JsonResponse(quen)
    else:
        return JsonResponse({'status': 0})

def SUBMIT(request, slug):
    ppr = Ppr.objects.get(new_slug = slug)
    time = Time.objects.filter(student = request.user, course = ppr.course, ppr=ppr).delete()
    time = Time(student = request.user, course = ppr.course, ppr=ppr, time = 0 )
    
    time.save()
    correct_answer = Ans.objects.filter(student = request.user, course = ppr.course, ppr=ppr, score = 1).count()
    wrong_answer = Ans.objects.filter(student = request.user, course = ppr.course, ppr=ppr, score = -1).count()
    not_answer = Ans.objects.filter(student = request.user, course = ppr.course, ppr=ppr, score = 0).count()
    result = Result(student = request.user, course = ppr.course, ppr=ppr, correct_answer= correct_answer, wrong_answer = wrong_answer, not_answer = not_answer)
    result.save()
    print(result)
    context = {
        'result' : result,
    }
    return render(request, "test/submit.html", context)
    

def QUESTIONS(request, slug):
    ppr = Ppr.objects.get(new_slug = slug)
    que = Que.objects.filter(ppr=ppr)
    paginator=Paginator(que, 1)
    page_number = request.GET.get('page', 1)
    que = paginator.get_page(page_number)
    quen = Que.objects.filter(qs_no=page_number, ppr=ppr)[0]
    time = Time.objects.filter(student=request.user, ppr=ppr)
    
    if time:
        pass
    else:
        time = Time(student=request.user,  ppr=ppr, time=ppr.time_duration * 60 * 1000)
        time.save()
    time_n = Time.objects.filter(student=request.user, ppr=ppr)
    for i in time_n:
        print(i.time)
        
    
    if request.method=='POST':
            getqs=Ans.objects.filter(que=quen, student=request.user, ppr=ppr).delete()
            
            form=AnsnChoice(request.POST or None)
            if form.is_valid():
                quens = Que.objects.filter(qs_no=page_number, ppr=ppr)
                for a in quens:
                    print(a.answers)
                    print(a.qs_no)
                ansn=form.cleaned_data.get('ansn')
                print(ansn)
                if ansn==a.answers:
                    ans = Ans(student=request.user,que_no=a.qs_no, que=quen, ppr=ppr, answer=ansn, correct_answer=a.answers, score=1)
                    ans.save()
                elif ansn!=a.answers:
                    ans = Ans(student=request.user,que_no=a.qs_no, que=quen, ppr=ppr, answer=ansn, correct_answer=a.answers, score=-1)
                    ans.save()
                else:
                    ans = Ans(student=request.user,que_no=a.qs_no, que=quen, ppr=ppr, answer=ansn, correct_answer=a.answers, score=0)
                    ans.save()
    ansnfrm=AnsnChoice()
    context = {
        'ansnfrm' : ansnfrm,
        'ppr' : ppr,
        'que' :que,
        'time_n' : time_n,        
    }
    return render(request, "profile/question_n.html", context)

def RESULT(request, slug):
    ppr = Ppr.objects.get(new_slug = slug)
    print(ppr)
    result = Result.objects.filter(student = request.user, ppr = ppr)
    print(result)
    if(result):
        pass
    else:
        correct_answer = Ans.objects.filter(ppr=ppr, score=1).count()
        wrong_answer = Ans.objects.filter(ppr=ppr, score=-1).count()
        print(wrong_answer)
        not_answer = Ans.objects.filter(ppr=ppr, score=0).count()
        print(not_answer)
        result = Result(student = request.user, ppr = ppr, correct_answer = correct_answer, wrong_answer = wrong_answer, not_answer = not_answer)
        result.save()
    context={
        'result': result,
        'ppr': ppr,
        'time' : time
    }
    return render(request, 'profile/result.html', context)


def SCORE_CARD(request, slug):
    
    ppr = Ppr.objects.get(new_slug = slug)
    print(ppr.title)
    ans = Ans.objects.filter(student = request.user, ppr = ppr)
    context={
        'ans':ans,
        'ppr' : ppr,
    }
    return render(request, 'profile/score_card.html', context)


    
def MY_VIDEOS(request):
    course = UserCourse.objects.filter(user = request.user)
    category = Categories.get_all_category(Categories)
    context = {
        'course': course,
        'category': category,
    }
    return render(request,'profile/my_videos.html', context)

def MY_VIDEOS_SLUG(request, slug):
    course = Course.objects.get(slug = slug)
    print(course)
    subject = Subject.objects.filter(course = course)
    print(subject)
    category = Categories.get_all_category(Categories)
    context = {
    'course' : course,
    'category' : category,
    'subject' : subject
    }
    return render(request, "profile/my_videos_d.html", context)

def video_lecture(request, slug):
    subject = Subject.objects.get(slug_s = slug)
    print(subject)
    context = {
        'subject' : subject,
    }
    return render(request,"profile/my_videos_sub.html", context)



def MY_E_BOOKS(request):
    course = UserCourse.objects.filter(user = request.user)
    category = Categories.get_all_category(Categories)
    context = {
        'course': course,
        'category': category,

    }
    return render(request,'profile/my_e-books.html', context)



def MY_E_BOOKS_SLUG(request, slug):
    course = Course.objects.get(slug = slug)
    subject = Subject.objects.filter(course = course)
    print(subject)
    category = Categories.get_all_category(Categories)
    context = {
    'course' : course,
    'category' : category,
    'subject' : subject
    }
    return render(request, "profile/my_e-books_d.html", context)


def E_BOOK(request, slug):
    subject = Subject.objects.get(slug_s = slug)
    print(subject)
    
    context ={
        'subject' : subject,
    }
    return render(request, "profile/e_book_sub.html", context)





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
    try:
        exam=Answer.objects.filter(student=request.user)[0].question
        
    except:
        msg="Select Course And Paper"
    if request.method=='POST':
        form=ExamChoiceFrm(request.POST or None)
        if form.is_valid():
            
            test=Test.objects.filter(test=form.cleaned_data.get('test'))[0]
            request.session['test']=test.id
            paper=Paper.objects.filter(paper=form.cleaned_data.get('paper'))[0]
            request.session['paper']=paper.id
            if test == exam.test and paper == exam.paper:
                form=ExamChoiceFrm()
                context={
                    'form': form,
                    'msg': 'Exam Already Completed' ,
                }
                return render(request, 'profile/test_series.html', context)
                
            else:
                try:
                    qs = Questions.objects.filter(test=test, paper=paper)
                    context ={
                        'questions': qs,
                        'qs': qs[0],
                    }
                    return render(request, 'profile/question.html', context)
                except:
                    form=ExamChoiceFrm()
                    context={
                        'form': form,
                        'msg': 'No Question Paper Found' ,
                    }
                    return render(request, 'profile/test_series.html', context)
    form=ExamChoiceFrm()
    msg=""
    context={
        'form': form,
        'msg': msg,
    }
    return render(request, 'profile/test_series.html', context)

def MY_PROFILE(request):
    return render(request, 'profile/my_profile.html')



def exam_home(request, qno):
    paper=request.session['paper']
    test=request.session['test']
    qts= Questions.objects.filter(test=test, paper=paper)
    try:
        qs=Questions.objects.filter(qs_no=qno)[0]
    except:
        qs=Questions.objects.filter(qs_no=1)[0]
    getqs=Answer.objects.filter(question=qs, student=request.user)
    print(getqs)
    if getqs:
        msg="Already Answered"
        request.session['msg']=msg
    else:
        if request.method=='POST':
            form=AnsChoice(request.POST or None)
            if form.is_valid():
                ans=form.cleaned_data.get('ans')
                ansqs = Answer (
                    student=request.user,
                    question=qs,
                    answer=ans
                )
                ansqs.save()
                nqno=int(qno) + 1
                print(nqno)
                request.session['msg']="Ans Saved Successfully"
                return redirect('exam_home', nqno)
    ansfrm= AnsChoice()
    context ={
        'ansfrm': ansfrm,
        'questions': qts,
        'qs': qs,
        }
    return render(request, 'profile/question.html', context)
    