# Generated by Django 3.2.9 on 2021-12-03 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0028_delete_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=32)),
                ('time', models.DateTimeField(default=True)),
                ('ex_num', models.CharField(max_length=32)),
                ('lot', models.CharField(max_length=32)),
                ('workshop', models.CharField(max_length=32)),
                ('mrb_list', models.CharField(max_length=32)),
                ('or_list', models.CharField(max_length=128)),
                ('ex_type', models.CharField(max_length=32)),
                ('ex_detail', models.CharField(max_length=32)),
                ('ex_number', models.CharField(max_length=32)),
                ('op_head', models.CharField(max_length=32)),
                ('op_unit', models.CharField(max_length=32)),
                ('client_type', models.CharField(max_length=32)),
                ('client_name', models.CharField(max_length=128)),
                ('des', models.CharField(max_length=1024)),
                ('des_confirm', models.CharField(max_length=1024)),
                ('improve', models.CharField(max_length=512)),
                ('effect_confirm', models.CharField(max_length=512)),
                ('op_dispose', models.CharField(max_length=32)),
            ],
        ),
    ]
