from django.contrib import admin

# Register your models here.
from .models import *
class Course_Features_TabularInline(admin.TabularInline):
    model = Course_Features

class Requirements_TabularInline(admin.TabularInline):
    model = Requirements

class Video_TabularInline(admin.TabularInline):
    model = Video

class course_admin(admin.ModelAdmin):
    inlines = ( Course_Features_TabularInline, Requirements_TabularInline, Video_TabularInline )
admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course, course_admin)
admin.site.register(Level)
admin.site.register(Course_Features)
admin.site.register(Requirements)
admin.site.register(Video)
admin.site.register(Lesson)
admin.site.register(Language)
admin.site.register(UserCourse)
admin.site.register(Payment)
admin.site.register(Contact)