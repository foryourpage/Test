# Generated by Django 3.2.9 on 2021-12-01 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0011_rename_create_time_article_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
