# Generated by Django 4.1.3 on 2023-02-07 10:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0047_alter_ans_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='time',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.course'),
        ),
    ]