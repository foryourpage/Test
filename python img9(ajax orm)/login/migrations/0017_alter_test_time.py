# Generated by Django 3.2.9 on 2021-12-03 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0016_alter_test_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='time',
            field=models.DateTimeField(default=True),
        ),
    ]
