from django.contrib import admin

# Register your models here.
from .models import *
class Course_Features_TabularInline(admin.TabularInline):
    model = Course_Features

class Requirements_TabularInline(admin.TabularInline):
    model = Requirements

class Video_TabularInline(admin.TabularInline):
    model = Video

class Ppr_TabularInline(admin.TabularInline):
    model = Ppr

class Que_Inline(admin.TabularInline):
    model = Que

class Video_Lecture_Inline(admin.TabularInline):
    model = Video_Lecture

class E_Book_Inline(admin.TabularInline):
    model = E_Book


class course_admin(admin.ModelAdmin):
    inlines = ( Course_Features_TabularInline, Requirements_TabularInline, Video_TabularInline, Ppr_TabularInline)

class ppr_admin(admin.ModelAdmin):
    inlines = [
        Que_Inline
    ]

class subject_admin(admin.ModelAdmin):
    inlines = [
        Video_Lecture_Inline,
        E_Book_Inline
    ]


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
# admin.site.register(Payment)
admin.site.register(Contact)
# admin.site.register(Test)
# admin.site.register(Paper)
# admin.site.register(Questions)
# admin.site.register(Answer)
admin.site.register(Ppr, ppr_admin)
admin.site.register(Que)
admin.site.register(Ans)
admin.site.register(Result)
admin.site.register(Time)
admin.site.register(Subject, subject_admin)
admin.site.register(Video_Lecture)
admin.site.register(E_Book)