# Generated by Django 4.1.3 on 2023-01-23 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_ans_correct_answer_ans_que_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='time',
            field=models.IntegerField(default=0),
        ),
    ]
