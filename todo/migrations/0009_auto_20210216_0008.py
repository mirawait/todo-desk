# Generated by Django 3.1.5 on 2021-02-15 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0008_auto_20210210_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_end',
            field=models.DateTimeField(default='15.02.2021 17:08'),
        ),
    ]