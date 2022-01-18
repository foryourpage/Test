# Generated by Django 3.2.9 on 2021-12-01 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_delete_article'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='Title', max_length=32)),
                ('content', models.TextField(null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
