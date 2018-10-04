# Generated by Django 2.1.1 on 2018-10-01 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='version',
            name='number',
        ),
        migrations.AddField(
            model_name='version',
            name='project',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='user_app.Project'),
        ),
        migrations.AddField(
            model_name='version',
            name='version',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='project',
            name='createTime',
            field=models.DateField(auto_now_add=True),
        ),
    ]
