# Generated by Django 4.1.3 on 2023-03-04 05:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0061_delete_payment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0002_payment_n_delete_payment_m'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Payment_n',
            new_name='Payment',
        ),
    ]