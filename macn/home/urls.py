from django.contrib import admin
from django.urls import path, include
from home import views, user_login
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.home, name="home"),
    path('404', views.PAGE_NOT_FOUND, name= "404"),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('courses', views.single_course, name="single_course"),
    path('courses/filter-data',views.filter_data,name="filter-data"),
    path('course/<slug:slug>', views.COURSE_DETAILS, name="course_details"),
    path('search', views.SEARCH_COURSE, name='search_course'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register', user_login.REGISTER, name= "register"),
    path('dologin', user_login.DO_LOGIN, name= "dologin"),
    path('accounts/profile', user_login.PROFILE, name= "profile"),
    path('accounts/profile/update', user_login.PROFILE_UPDATE, name= "profile_update"),
    path('checkout/<slug:slug>', views.CHECKOUT, name="checkout"),
    path('verify_payment', views.VERIFY_PAYMENT, name="verify_payment"),
    path('course/watch-course/<slug:slug>', views.WATCH_COURSE, name="watch_course"),
    path('test-series', views.TEST_SERIES, name="test_series"),
    path('my_profile', views.MY_PROFILE, name="my_profile"),
    path('Questions/<int:qno>', views.exam_home, name='exam_home'),
    path('my-course', views.MY_COURSE, name="my_course"),
    path('my-course/<slug:slug>', views.MY_COURSE_SLUG, name='my_course_slug'),
    path('my-test-series', views.MY_TEST_SERIES, name="my_test_series"),
    path('my-test-series/<slug:slug>', views.MY_TEST_SERIES_SLUG, name="my_test_series_slug"),
    path('instructions/<slug>', views.instructions, name="instructions"),
    path('result_explanation/<slug>', views.result_d, name="result_d"),
    path('Question/<slug>', views.Question, name="Question"),
    path('submit/<slug>', views.SUBMIT, name="submit"),
    path('Questions/<slug>', views.QUESTIONS, name="questions"),
    path('my-videos', views.MY_VIDEOS, name="my_videos"),
    path('my-videos/<slug:slug>', views.MY_VIDEOS_SLUG, name="my_videos_slug"),
    path('my-videos/video_lecture/<slug>', views.video_lecture, name="video_lecture"),
    path('my-e-books', views.MY_E_BOOKS, name="my_e-books"),
    path('my-e-books/<slug:slug>', views.MY_E_BOOKS_SLUG, name="my_e-books"),
    path('my-e-books/e-book/<slug>', views.E_BOOK, name="e-book"),
    
    path('result/<slug>', views.RESULT, name="result"),
    path('score_card/<slug>', views.SCORE_CARD, name="score_card"),
    path('number/', views.number_que, name="number"),
    path('next/', views.next_que, name="next"),
    path('mark/', views.mark_que, name="mark"),
    path('que_page/', views.que_page, name="que_page"),

    
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
