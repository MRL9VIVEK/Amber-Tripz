# Generated by Django 4.1.3 on 2023-02-24 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0055_usercourse_expiry_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercourse',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
