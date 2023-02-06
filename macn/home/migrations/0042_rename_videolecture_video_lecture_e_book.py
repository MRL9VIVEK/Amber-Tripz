# Generated by Django 4.1.3 on 2023-02-04 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_rename_name_subject_subject_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='VideoLecture',
            new_name='Video_Lecture',
        ),
        migrations.CreateModel(
            name='E_Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.IntegerField(null=True)),
                ('thumbnail', models.ImageField(null=True, upload_to='Media/lecture')),
                ('title', models.CharField(max_length=300)),
                ('book', models.FileField(null=True, upload_to='Media/video')),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.course')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.subject')),
            ],
        ),
    ]