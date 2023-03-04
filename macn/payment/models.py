from django.db import models
from django.contrib.auth.models import User
from home.models import Course, UserCourse

# Create your models here.

class Payment(models.Model):
    order_id = models.CharField(max_length=100,null=True, blank=True)
    payment_id = models.CharField(max_length=100,null=True, blank=True)
    signature_id = models.CharField(max_length=100,null=True, blank=True)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.user.first_name + " " + self.course.title