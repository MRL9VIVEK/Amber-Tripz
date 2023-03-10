from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.conf import settings
from autoslug import AutoSlugField

# Create your models here.
class Categories(models.Model):
    
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='home/images', default="")

    def __str__(self):
        return self.name

    def get_all_category(self):
        return Categories.objects.all().order_by('id')

class Author(models.Model):
    author_profile = models.ImageField(upload_to="Media/author")
    name = models.CharField(max_length=100, null=True)
    field = models.CharField(max_length=100, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language

class Course(models.Model):
    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )

    featured_image = models.ImageField(upload_to="Media/featured_img",null=True)
    featured_video = models.CharField(max_length=300,null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    level = models.ForeignKey(Level,on_delete=models.CASCADE,null=True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    DeadLine = models.CharField(max_length=500, null=True)
    language = models.ForeignKey(Language,on_delete=models.CASCADE,null=True)
    status = models.CharField(choices=STATUS,max_length=100,null=True)
    validity = models.CharField(max_length=100,null=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_details", kwargs={'slug': self.slug})

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)


class Course_Features(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=300)

    def __str__(self):
        return self.points

class Requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=300)

    def __str__(self):
        return self.points


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " = " + self.course.title


class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/Yt_Thumbnail", null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    youtube_id = models.CharField(max_length=300)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
class Subject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    thumbnail = models.ImageField(upload_to="Media/subject", null=True)
    subject_name = models.CharField(max_length=200)
    title = models.CharField(max_length=300, null=True)
    total_que = models.CharField(max_length=300, null=True)
    total_marks = models.CharField(max_length=300, null=True)
    slug_s = AutoSlugField(populate_from='title', unique=True, null=True, default=None)
    

    def __str__(self):
        return self.subject_name + " = " + self.course.title
    
    
class Video_Lecture(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/lecture", null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300)
    video = models.FileField(upload_to="Media/video", null=True)

    def __str__(self):
        return self.title
    
class E_Book(models.Model):
    serial_number = models.IntegerField(null=True)
    thumbnail = models.ImageField(upload_to="Media/lecture", null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300)
    book = models.FileField(upload_to="Media/book", null=True)

    def __str__(self):
        return self.title


class Ppr(models.Model):
    serial_number = models.IntegerField(null=True)
    title = models.CharField(max_length=300, null=True)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True)
    new_slug = AutoSlugField(populate_from='title', unique=True, null=True, default=None)
    
    time_duration = models.IntegerField(null=True)
    

    def __str__(self):
        return self.title

class Que(models.Model):
    id = models.AutoField(primary_key=True)
    qs_no=models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    ppr = models.ForeignKey(Ppr, on_delete=models.CASCADE,null=True)
    subject = models.CharField(max_length=300, null=True)
    questions=models.TextField(null=True)
    image = models.ImageField(upload_to='Media/que', blank=True, null=True)
    answers=models.CharField(max_length=20, null=True)
    option_a=models.TextField(null=True)
    image_a = models.ImageField(upload_to='Media/ans', blank=True, null=True)
    option_b=models.TextField(null=True)
    image_b = models.ImageField(upload_to='Media/ans', blank=True, null=True)
    option_c=models.TextField(null=True)
    image_c = models.ImageField(upload_to='Media/ans', blank=True, null=True)
    option_d=models.TextField(null=True)
    image_d = models.ImageField(upload_to='media/ans', blank=True, null=True)
    disc=models.TextField(null=True)
    def __str__(self):
        return 'Q.'+ str(self.qs_no)  + ')  '+  self.questions


class Ans(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null= True)
    ppr=models.ForeignKey(Ppr,on_delete=models.CASCADE, null=True)
    que_no=models.IntegerField(default=1)
    que=models.ForeignKey(Que,on_delete=models.CASCADE)
    answer=models.CharField(max_length=20, null=True)
    correct_answer=models.CharField(max_length=20, null=True)
    mark = models.IntegerField(default=0)
    score=models.FloatField(default=0)
    # date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.answer

class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null=True)
    ppr=models.ForeignKey(Ppr,on_delete=models.CASCADE, null=True)
    correct_answer=models.IntegerField(default=0)
    wrong_answer=models.IntegerField(default=0)
    not_answer=models.IntegerField(default=0)
    
    def __str__(self):
        return self.student.username
    
class Time(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE, null= True)
    ppr = models.ForeignKey(Ppr,on_delete=models.CASCADE, null=True)
    time = models.IntegerField(default=0)
    def __str__(self):
        return self.student.username

        
class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=1)
    expiry_date = models.DateTimeField(null=True, blank=True)
    

    def __str__(self):
        return self.user.first_name + " " + self.course.title




# class Payment(models.Model):
#     order_id = models.CharField(max_length=100,null=True, blank=True)
#     payment_id = models.CharField(max_length=100,null=True, blank=True)
#     signature_id = models.CharField(max_length=100,null=True, blank=True)
#     user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
#     date = models.DateTimeField(auto_now_add=True)
#     status = models.BooleanField(default=False)

#     def __str__(self):
#         return self.user.first_name + " " + self.course.title


class Contact(models.Model):
    name = models.CharField(max_length=50,null=True, blank=True)
    email = models.CharField(max_length=70, null=True, blank=True)
    desc = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.email


class Test(models.Model):
    test=models.CharField(max_length=150,unique=True)
    
    def __str__(self):
        return self.test
class Paper(models.Model):
    paper=models.CharField(max_length=150)

    def __str__(self):
        return self.paper

class Questions(models.Model):
    qs_no=models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    test=models.ForeignKey(Test,on_delete=models.CASCADE)
    paper=models.ForeignKey(Paper,on_delete=models.CASCADE)
    questions=models.TextField()

    answers=models.CharField(max_length=20)
    option_a=models.TextField()
    option_b=models.TextField()
    option_c=models.TextField()
    option_d=models.TextField()
    def __str__(self):
        return 'Q.'+ str(self.qs_no)  + ')  '+  self.questions


class Answer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    
    question=models.ForeignKey(Questions,on_delete=models.CASCADE)
    answer=models.CharField(max_length=20)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.answer

    
    