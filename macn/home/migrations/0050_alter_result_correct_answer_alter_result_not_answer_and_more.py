# Generated by Django 4.1.3 on 2023-02-08 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0049_result_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='correct_answer',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='result',
            name='not_answer',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='result',
            name='wrong_answer',
            field=models.IntegerField(default=0),
        ),
    ]
