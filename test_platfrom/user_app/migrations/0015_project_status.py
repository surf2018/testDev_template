# Generated by Django 2.1.1 on 2018-10-10 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0014_auto_20181004_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.BooleanField(default=True, verbose_name='status:'),
        ),
    ]
