# Generated by Django 4.1.3 on 2023-01-03 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_questions_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.course'),
        ),
    ]
