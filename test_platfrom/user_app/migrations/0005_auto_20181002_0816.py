# Generated by Django 2.1.1 on 2018-10-02 00:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0004_auto_20181002_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.Project'),
        ),
    ]