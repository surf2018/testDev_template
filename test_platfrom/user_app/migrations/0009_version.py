# Generated by Django 2.1.1 on 2018-10-02 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0008_auto_20181002_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=20)),
                ('description', models.TextField(max_length=50)),
                ('release', models.CharField(max_length=5)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.Project')),
            ],
        ),
    ]
