# Generated by Django 3.1.6 on 2021-03-25 15:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stlConverter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='saveContactData',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('fname', models.CharField(max_length=20)),
                ('lname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=35)),
                ('feedback', models.TextField(max_length=400)),
                ('contactDateTime', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.DeleteModel(
            name='saveDicomFiles',
        ),
    ]