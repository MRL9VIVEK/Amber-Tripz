from django.contrib.auth.models import User
from django import forms
from home.models import Questions, Ans
ANS_CHOICES= [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ]

ANSN_CHOICES= [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ]

class ExamChoiceFrm(forms.ModelForm):
    class Meta:
        model=Questions
        fields=[
            'course',
            'test',
            'paper',
        ]

class AnsChoice(forms.Form):
    ans= forms.CharField(label='Select a option', widget=forms.RadioSelect(choices=ANS_CHOICES))
    def clean(self,*args,**kwargs):
        ans=self.cleaned_data.get('ans')
        return super(AnsChoice,self).clean(*args,**kwargs)

class AnsnChoice(forms.Form):
    ansn= forms.CharField(label='Select a option', widget=forms.RadioSelect(choices=ANSN_CHOICES))
    def clean(self,*args,**kwargs):
        ansn=self.cleaned_data.get('ansn')
        return super(AnsnChoice,self).clean(*args,**kwargs)