# Generated by Django 3.1.5 on 2021-02-01 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20210201_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_end',
            field=models.DateTimeField(default='01.02.2021 09:41'),
        ),
    ]
