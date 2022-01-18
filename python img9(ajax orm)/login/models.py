from django.db import models


# Create your models here.

class User(models.Model):
    gender = (
        ('male', '男'),
        ('female', '女')
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Article(models.Model):
    title = models.CharField(max_length=32, default='Title')
    content = models.TextField(null=True)
    time = models.DateField(auto_now_add=True)


class Person(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    age = models.IntegerField(verbose_name='年龄')
    score = models.FloatField(verbose_name='成绩')


class Test(models.Model):
    state = models.CharField(max_length=32)
    time = models.DateTimeField(default=True)
    ex_num = models.CharField(max_length=32)
    lot = models.CharField(max_length=32)
    workshop = models.CharField(max_length=32)
    mrb_list = models.CharField(max_length=32)
    or_list = models.CharField(max_length=128)
    ex_type = models.CharField(max_length=32)
    ex_detail = models.CharField(max_length=32)
    ex_number = models.CharField(max_length=32)
    op_head = models.CharField(max_length=32)
    op_unit = models.CharField(max_length=32)
    client_type = models.CharField(max_length=32)
    client_name = models.CharField(max_length=128)
    des = models.CharField(max_length=1024)
    des_confirm = models.CharField(max_length=1024)
    improve = models.CharField(max_length=512)
    effect_confirm = models.CharField(max_length=512)
    op_dispose = models.CharField(max_length=32)

    def short_or_list(self):
        if len(str(self.or_list)) > 10:
            return '{}...'.format(str(self.or_list)[0:9])
        else:
            return str(self.or_list)

    short_or_list.allow_tags = True
    short_or_list.short_description = 'or_list详情'

    def short_client_name(self):
        if len(str(self.client_name)) > 10:
            return '{}...'.format(str(self.client_name)[0:9])
        else:
            return str(self.client_name)

    short_client_name.allow_tags = True
    short_client_name.short_description = 'client_name详情'

    def short_des(self):
        if len(str(self.des)) > 10:
            return '{}...'.format(str(self.des)[0:9])
        else:
            return str(self.des)

    short_des.allow_tags = True
    short_des.short_description = 'des详情'

    def short_des_confirm(self):
        if len(str(self.des_confirm)) > 10:
            return '{}...'.format(str(self.des_confirm)[0:9])
        else:
            return str(self.des_confirm)

    short_des_confirm.allow_tags = True
    short_des_confirm.short_description = 'des_confirm详情'

    def short_improve(self):
        if len(str(self.improve)) > 10:
            return '{}...'.format(str(self.improve)[0:9])
        else:
            return str(self.improve)

    short_improve.allow_tags = True
    short_improve.short_description = 'improve详情'

    def short_effect_confirm(self):
        if len(str(self.effect_confirm)) > 10:
            return '{}...'.format(str(self.effect_confirm)[0:9])
        else:
            return str(self.effect_confirm)

    short_effect_confirm.allow_tags = True
    short_effect_confirm.short_description = 'effect_confirm详情'

