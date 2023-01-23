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
    path('Questions/<slug>', views.QUESTIONS, name="questions"),
    path('my-videos', views.MY_VIDEOS, name="my_videos"),
    path('my-videos/<slug:slug>', views.MY_VIDEOS_SLUG, name="my_videos_slug"),
    path('my-e-books', views.MY_E_BOOKS, name="my_e-books"),
    path('my-e-books/<slug:slug>', views.MY_E_BOOKS_SLUG, name="my_e-books"),
    path('result/<slug>', views.RESULT, name="result"),
    path('score_card/<slug>', views.SCORE_CARD, name="score_card"),
    

    
]+ static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
