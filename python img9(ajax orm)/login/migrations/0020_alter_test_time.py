# Generated by Django 3.2.9 on 2021-12-03 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0019_alter_test_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='time',
            field=models.CharField(max_length=32),
        ),
    ]