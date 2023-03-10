# Generated by Django 4.1.3 on 2023-01-07 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_remove_ppr_subject_que_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ppr',
            name='preview',
        ),
        migrations.AddField(
            model_name='que',
            name='disc',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='que',
            name='time_duration',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ppr',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.course'),
        ),
        migrations.AlterField(
            model_name='que',
            name='answers',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='que',
            name='option_a',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='que',
            name='option_b',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='que',
            name='option_c',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='que',
            name='option_d',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='que',
            name='questions',
            field=models.TextField(null=True),
        ),
    ]
