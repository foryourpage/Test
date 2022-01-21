import json
import os
import re
from venv import logger

import xlrd
from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from numpy import long
from openpyxl import load_workbook
from scrapy import settings
from sqlalchemy import or_

from login import models
from .forms import UserForm
from .forms import RegisterForm

# Create your views here.
from .models import User, Test
from .models import Article
from .models import Person
from login import models
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime

from django.utils import timezone
from django.db import transaction
from xlrd import xldate_as_tuple
from django.db.models import Q
from collections import defaultdict


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def index(request):
    pass
    return render(request, 'login/test3.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "所有字段都必须填写！"
        if login_form.is_valid():  # 确保用户名和密码都不为空
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户名不存在！"
        return render(request, 'login/login.html', locals())
    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")


def book(request):
    return render(request, 'login/book.html')


def getdata(request):
    User_list = User.objects.all()
    datalist = serialize('json', User_list)
    json_data = json.loads(datalist)
    rows = []
    for i in range(len(json_data)):
        rows.append(json_data[i]['fields'])
    finalData = {
        "total": 800,
        'rows': rows
    }
    return JsonResponse(finalData, safe=False)


def img1(request):
    name_list = ['GLASS維護課', 'SEAM維護一課', 'SEAM維護二課', '工程部', '生產一部', '生產二部',
                 '生產部', '生產製程維護課', '材料品質部', '保養課', '品質工程部', '品質維護課', '設備維護一課', '設備維護二課',
                 '晶片產品工程課', '晶片製造工程課', '晶體工程課', '新產品品質部', '過程管控課', '製造一部', '製造二部', '製造三部',
                 '製造工程部', '製程維護一課', '製程維護二課', '製程維護三課', '廠務系統維護課', '檢加設備維護一課', '檢加維護課',
                 '檢加設備維護一課', '檢加製程維護課', '檢驗加工部']
    number = []
    for i in range(len(name_list)):
        number.append(models.Test.objects.filter(state="结案", op_unit=name_list[i]).count())
        data_dict = dict(zip(name_list, number))
    return render(request, 'login/img1.html', {'data_dict': json.dumps(data_dict)})


def home(request):
    return render(request, "login/home.html")


def img2(request):
    return render(request, 'login/img2.html')


def img3(request):
    return render(request, 'login/img3.html')


def img4(request):
    return render(request, 'login/img4.html')


@csrf_exempt
def all_table(request):
    if request.method == 'GET':
        page_size = int(request.GET['pageSize'])
        page_number = int(request.GET['pageNumber'])
        total = models.Article.objects.count()
        articles = models.Article.objects.order_by('-id')[(page_number - 1) * page_size:page_number * page_size]
        rows = []
        data = {'total': total, 'rows': rows}
        for article in articles:
            rows.append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'time': article.time
            })
        return HttpResponse(json.dumps(data, cls=ComplexEncoder), content_type='application/json')


@csrf_exempt
def add_article(request):
    ctx = {}
    if request.POST:
        ctx['title'] = request.POST['title']
        ctx['content'] = request.POST['content']
        test1 = models.Article(title=ctx['title'], content=ctx['content'])
        test1.save()
        data = {'ret': True, 'msg': '数据提交成功！'}
        return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def delete_article(request):
    article = models.Article.objects.get(id=request.POST['id'])
    article.delete()
    data = {'ret': True, 'msg': '删除成功！'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        f = request.FILES.get('file')
        excel_type = f.name.split('.')[1]
        # 这里的分隔可以取到对应的文件后缀
        if excel_type in ['xlsx', 'xls']:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows  # 总行数
            test_list = Test.objects.all()
            try:
                with transaction.atomic():  # 控制数据库事务交易
                    for i in range(1, rows):
                        rowVlaues = table.row_values(i)
                        rowVlaues2 = xldate_as_tuple(rowVlaues[1], 0)
                        # rowVlaues3 = datetime(*rowVlaues2).strftime('%Y/%m/%d %H:%M:%S')
                        rowVlaues3 = datetime(*rowVlaues2)
                        if test_list.filter(ex_num=rowVlaues[2]):
                            pass
                        else:
                            #  elif语句成功执行不会执行else语句
                            models.Test.objects.create(state=rowVlaues[0], time=rowVlaues3, ex_num=rowVlaues[2],
                                                       lot=rowVlaues[3], workshop=rowVlaues[4], mrb_list=rowVlaues[5],
                                                       or_list=rowVlaues[6], ex_type=rowVlaues[7],
                                                       ex_detail=rowVlaues[8],
                                                       ex_number=rowVlaues[9], op_head=rowVlaues[10],
                                                       op_unit=rowVlaues[11],
                                                       client_type=rowVlaues[12], client_name=rowVlaues[13],
                                                       des=rowVlaues[14],
                                                       des_confirm=rowVlaues[15], improve=rowVlaues[16],
                                                       effect_confirm=rowVlaues[17],
                                                       op_dispose=rowVlaues[18])
                        if test_list.filter(ex_num=rowVlaues[2]).exclude(state=rowVlaues[0],
                                                                         lot=rowVlaues[3], workshop=rowVlaues[4],
                                                                         mrb_list=rowVlaues[5],
                                                                         or_list=rowVlaues[6], ex_type=rowVlaues[7],
                                                                         ex_detail=rowVlaues[8],
                                                                         ex_number=rowVlaues[9], op_head=rowVlaues[10],
                                                                         op_unit=rowVlaues[11],
                                                                         client_type=rowVlaues[12],
                                                                         client_name=rowVlaues[13],
                                                                         des=rowVlaues[14],
                                                                         des_confirm=rowVlaues[15],
                                                                         improve=rowVlaues[16],
                                                                         effect_confirm=rowVlaues[17],
                                                                         op_dispose=rowVlaues[18]):
                            # 筛选条件一语句的数据,过滤掉满足所有条件的数据，当条件二发生相应的变化，过滤不掉所有数据，返回true
                            models.Test.objects.filter(ex_num=rowVlaues[2]).update(state=rowVlaues[0],
                                                                                   lot=rowVlaues[3],
                                                                                   workshop=rowVlaues[4],
                                                                                   mrb_list=rowVlaues[5],
                                                                                   or_list=rowVlaues[6],
                                                                                   ex_type=rowVlaues[7],
                                                                                   ex_detail=rowVlaues[8],
                                                                                   ex_number=rowVlaues[9],
                                                                                   op_head=rowVlaues[10],
                                                                                   op_unit=rowVlaues[11],
                                                                                   client_type=rowVlaues[12],
                                                                                   client_name=rowVlaues[13],
                                                                                   des=rowVlaues[14],
                                                                                   des_confirm=rowVlaues[15],
                                                                                   improve=rowVlaues[16],
                                                                                   effect_confirm=rowVlaues[17],
                                                                                   op_dispose=rowVlaues[18])
            except Exception as e:
                print("error", e)
                logger.error('解析excel文件或者数据插入错误')
            return render(request, 'login/img2.html', {'message': '导入成功'})
        else:
            logger.error('上传文件类型错误！')
            return render(request, 'login/img2.html', {'message': '导入失败'})


@csrf_exempt
def all_form(request):
    if request.method == 'GET':
        page_size = int(request.GET['pageSize'])
        page_number = int(request.GET['pageNumber'])
        startTime = request.GET['startTime']
        if len(startTime) == 12:
            startTime = '0' + startTime
        if startTime == 'NaN':
            startTime2 = '1999-08-26 00:00'
        else:
            startTime = startTime[0:10]
            startTime = int(startTime)  # 转化为数字形式
            startTime = datetime.fromtimestamp(startTime)  # 转化为日期格式
            startTime2 = startTime.strftime('%Y-%m-%d %H:%M:%S.%f')  # 精确到秒、毫秒

        endTime = request.GET['endTime']
        if len(endTime) == 12:
            endTime = '0' + endTime
        if endTime == 'NaN':
            d1 = timezone.now()
            endTime2 = d1.strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            endTime = endTime[0:10]
            endTime = int(endTime)
            endTime = datetime.fromtimestamp(endTime)
            endTime2 = endTime.strftime('%Y-%m-%d %H:%M:%S.%f')

        ex_num = request.GET['ex_num']
        lot = request.GET['lot']
        op_unit = request.GET['op_unit']
        total = models.Test.objects.filter(time__range=[startTime2, endTime2], ex_num__contains=ex_num,
                                           lot__contains=lot, op_unit__contains=op_unit).count()
        Tests = models.Test.objects.filter(time__range=[startTime2, endTime2], ex_num__contains=ex_num,
                                           lot__contains=lot, op_unit__contains=op_unit).order_by('-time')[
                (page_number - 1) * page_size:page_number * page_size]

        rows = []
        data = {'total': total, 'rows': rows}
        for test in Tests:
            rows.append({
                'id': test.id,
                'state': test.state,
                'time': test.time,
                'ex_num': test.ex_num,
                'lot': test.lot,
                'workshop': test.workshop,
                'mrb_list': test.mrb_list,
                'or_list': test.or_list,
                'ex_type': test.ex_type,
                'ex_detail': test.ex_detail,
                'ex_number': test.ex_number,
                'op_head': test.op_head,
                'op_unit': test.op_unit,
                'client_type': test.client_type,
                'client_name': test.client_name,
                'des': test.des,
                'des_confirm': test.des_confirm,
                'improve': test.improve,
                'effect_confirm': test.effect_confirm,
                'op_dispose': test.op_dispose
            })
        return HttpResponse(json.dumps(data, cls=ComplexEncoder), content_type='application/json')


@csrf_exempt
def delete_test(request):
    test = models.Test.objects.get(id=request.POST['id'])
    test.delete()
    data = {'ret': True, 'msg': '删除成功！'}
    return HttpResponse(json.dumps(data), content_type='application/json')


@csrf_exempt
def statistics(request):
    if request.POST:
        data_year = request.POST['data_year']
        number = []
        for i in range(1, 13):
            number.append(models.Test.objects.filter(time__year=data_year, time__month=i).exclude(state="放弃").count())
        data = {'number': number}
    return HttpResponse(json.dumps(data), content_type="application/json")


def img5(request):
    name_list = ['1.1驗證異常', '1.其他', '1.品質檢驗異常', '2.產線異常', '4.客訴需求', '5.改善性驗證', '材料异常', '品質檢驗異常',
                 '產線異常', '産缐異常', ' ']
    number = []
    for i in range(len(name_list)):
        number.append(models.Test.objects.filter(ex_type=name_list[i]).count())
    data_dict = dict(zip(name_list, number))
    data_dict = sorted(data_dict.items(), key=lambda d: d[1], reverse=False)
    # 对应的.items我们可以把键值对放到元组里去  后面是匿名函数,获取每一个元组的第二个元素,进行对应的翻转
    data_dict = dict(data_dict)
    return render(request, 'login/img5.html', {'data_dict': json.dumps(data_dict)})


def img6(request):
    return render(request, 'login/img6.html')


@csrf_exempt
def percentage(request):
    if request.POST:
        data_year = request.POST['data_year']
        number = []
        number1 = []
        for i in range(1, 13):
            number1.append(models.Test.objects.filter(time__year=data_year, time__month=i).exclude(state="放弃").count())
            number2 = models.Test.objects.filter(time__year=data_year, time__month=i, state="结案").count()
            number3 = models.Test.objects.filter(time__year=data_year, time__month=i).exclude(state="放弃").count()
            if number3 == 0:
                percentage2 = 0
            else:
                percentage2 = (number2 / number3) * 100
            percentage2 = round(percentage2, 2)
            print(percentage2)
            number.append(percentage2)
        data = {'number': number, 'number1': number1}
        return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def img7(request):
    if request.POST:
        startTime = request.POST['startTime']
        if len(startTime) == 12:
            startTime = '0' + startTime
        if startTime == 'NaN':
            startTime2 = '1999-08-26 00:00'
        else:
            startTime = startTime[0:10]
            startTime = int(startTime)
            startTime = datetime.fromtimestamp(startTime)
            startTime2 = startTime.strftime('%Y-%m-%d %H:%M:%S.%f')

        endTime = request.POST['endTime']
        if len(endTime) == 12:
            endTime = '0' + endTime
        if endTime == 'NaN':
            d1 = timezone.now()
            endTime2 = d1.strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            endTime = endTime[0:10]
            endTime = int(endTime)
            endTime = datetime.fromtimestamp(endTime)
            endTime2 = endTime.strftime('%Y-%m-%d %H:%M:%S.%f')
        print(startTime2)
        print(endTime2)
        number = []
        name_list2 = []
        test = models.Test.objects.filter(time__range=[startTime2, endTime2], state="结案").values_list('op_unit',
                                                                                                      flat=True).distinct()
        for i in range(len(test)):
            name_list2.append(test[i])
        print(name_list2)
        print(len(name_list2))
        for i in range(len(name_list2)):
            number.append(models.Test.objects.filter(time__range=[startTime2, endTime2], op_unit=name_list2[i],
                                                     state="结案").count())
        data_dict = dict(zip(name_list2, number))
        data_dict = sorted(data_dict.items(), key=lambda d: d[1], reverse=True)
        # 对应的.items我们可以把键值对放到元组里去  后面是匿名函数,获取每一个元组的第二个元素,进行对应的翻转
        data_dict = dict(data_dict)
        print(data_dict)
        return HttpResponse(json.dumps(data_dict), content_type="application/json")  # HttpResponse需要对数据进行序列化
        # return JsonResponse(data_dict)   #JsonResponse则不需要进行序列化
    return render(request, 'login/img7.html')


@csrf_exempt
def img8(request):
    if request.POST:
        chk_value = request.POST.get('chk_value')
        chk_value = json.loads(chk_value)
        startTime = request.POST['startTime']
        if len(startTime) == 12:
            startTime = '0' + startTime
        if startTime == 'NaN':
            startTime2 = '1999-08-26 00:00'
        else:
            startTime = startTime[0:10]
            startTime = int(startTime)
            startTime = datetime.fromtimestamp(startTime)
            startTime2 = startTime.strftime('%Y-%m-%d %H:%M:%S.%f')

        endTime = request.POST['endTime']
        if len(endTime) == 12:
            endTime = '0' + endTime
        if endTime == 'NaN':
            d1 = timezone.now()
            endTime2 = d1.strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            endTime = endTime[0:10]
            endTime = int(endTime)
            endTime = datetime.fromtimestamp(endTime)
            endTime2 = endTime.strftime('%Y-%m-%d %H:%M:%S.%f')
        number = []
        number2 = []
        name_list2 = []
        # dict2 = defaultdict(list)
        dict2 = {}
        if len(chk_value):
            test = models.Test.objects.filter(time__range=[startTime2, endTime2]).exclude(state="放弃").values_list(
                'op_unit', flat=True).distinct()
            test = test.filter(op_unit__in=chk_value)
        else:
            test = models.Test.objects.filter(time__range=[startTime2, endTime2]).exclude(state="放弃").values_list(
                'op_unit', flat=True).distinct()

        for i in range(len(test)):
            name_list2.append(test[i])
        for i in range(len(name_list2)):
            number.append(models.Test.objects.filter(time__range=[startTime2, endTime2], op_unit=name_list2[i],
                                                     state="结案").count())

        for i in range(len(name_list2)):
            number2.append(
                models.Test.objects.filter(time__range=[startTime2, endTime2], op_unit=name_list2[i]).exclude(
                    Q(state="结案") | Q(state="放弃")).count()
            )

        for i in range(len(name_list2)):
            # dict2[name_list2[i]].append(number[i])
            # dict2[name_list2[i]].append(number2[i])
            dict2[name_list2[i]] = []
            dict2[name_list2[i]].append(str(number[i]))
            dict2[name_list2[i]].append(str(number2[i]))
        data = {'name_list2': name_list2, 'number': number, 'number2': number2}
        dict2 = sorted(dict2.items(), key=lambda item: (int(item[1][0]), int(item[1][1])), reverse=True)
        # 每个item里面有两个下标，零和一，我们取后面的，再按照下标取
        dict2 = dict(dict2)
        keys = dict2.keys()
        keys = list(keys)
        values = dict2.values()
        values = list(values)
        number3 = []
        number4 = []
        for i in range(len(values)):
            number3.append(values[i][0])
            number4.append(values[i][1])
        data2 = {'keys': keys, 'number3': number3, 'number4': number4}
        return HttpResponse(json.dumps(data2), content_type="application/json")  # HttpResponse需要对数据进行序列化
    return render(request, 'login/img8.html')


def img9(request):
    return render(request, 'login/img9.html')


def imh(request):
    return render(request, 'login/imh.html')


@csrf_exempt
def imj(request):
    if request.POST:
        startTime = request.POST['startTime']
        if len(startTime) == 12:
            startTime = '0' + startTime
        if startTime == 'NaN':
            startTime2 = '1999-08-26 00:00'
        else:
            startTime = startTime[0:10]
            startTime = int(startTime)
            startTime = datetime.fromtimestamp(startTime)
            startTime2 = startTime.strftime('%Y-%m-%d %H:%M:%S.%f')

        endTime = request.POST['endTime']
        if len(endTime) == 12:
            endTime = '0' + endTime
        if endTime == 'NaN':
            d1 = timezone.now()
            endTime2 = d1.strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            endTime = endTime[0:10]
            endTime = int(endTime)
            endTime = datetime.fromtimestamp(endTime)
            endTime2 = endTime.strftime('%Y-%m-%d %H:%M:%S.%f')
        number = []
        name_list2 = []
        test = models.Test.objects.filter(time__range=[startTime2, endTime2]).exclude(
            Q(state="结案") | Q(state="放弃")).values_list('op_unit',
                                                       flat=True).distinct()
        for i in range(len(test)):
            name_list2.append(test[i])
        for i in range(len(name_list2)):
            number.append(models.Test.objects.filter(time__range=[startTime2, endTime2], op_unit=name_list2[i]).exclude(
                Q(state="结案") | Q(state="放弃")).count())
        data_dict = dict(zip(name_list2, number))
        data_dict = sorted(data_dict.items(), key=lambda d: d[1], reverse=True)
        # 对应的.items我们可以把键值对放到元组里去  后面是匿名函数,获取每一个元组的第二个元素,进行对应的翻转
        data_dict = dict(data_dict)
        print(data_dict)
        return HttpResponse(json.dumps(data_dict), content_type="application/json")  # HttpResponse需要对数据进行序列化
        # return JsonResponse(data_dict)   #JsonResponse则不需要进行序列化
    return render(request, 'login/imj.html')


def imk(request):
    name_list = []
    test = models.Test.objects.exclude(state="放弃").values_list('ex_type', flat=True).distinct()
    for i in range(len(test)):
        name_list.append(test[i])
    number = []
    for i in range(len(name_list)):
        number.append(models.Test.objects.filter(ex_type=name_list[i]).count())
    data_dict = dict(zip(name_list, number))
    data_dict = sorted(data_dict.items(), key=lambda d: d[1], reverse=False)
    # 对应的.items我们可以把键值对放到元组里去  后面是匿名函数,获取每一个元组的第二个元素,进行对应的翻转
    data_dict = dict(data_dict)

    name_list2 = []
    number2 = []
    test2 = models.Test.objects.filter(state="结案").values_list('op_unit', flat=True).distinct()
    for i in range(len(test2)):
        name_list2.append(test2[i])
    for i in range(len(name_list2)):
        number2.append(models.Test.objects.filter(op_unit=name_list2[i]).count())
    data_dict2 = dict(zip(name_list2, number2))
    data_dict2 = sorted(data_dict2.items(), key=lambda d: d[1], reverse=False)
    data_dict2 = dict(data_dict2)

    data_year = []
    data_dict3 = {}
    d1 = timezone.now().year
    d1 = d1 + 1
    for i in range(2019, d1):
        data_year.append(i)
    for i in range(len(data_year)):
        data_dict3[data_year[i]] = []
        for j in range(1, 13):
            data_dict3[data_year[i]].append(
                models.Test.objects.filter(time__year=data_year[i], time__month=j).exclude(state="放弃").count())

    name_list3 = []
    number3 = []
    number4 = []
    test3 = models.Test.objects.exclude(state="放弃").values_list('op_unit', flat=True).distinct()
    for i in range(len(test3)):
        name_list3.append(test3[i])
    for i in range(len(name_list3)):
        number3.append(models.Test.objects.filter(op_unit=name_list3[i],
                                                  state="结案").count())
    for i in range(len(name_list3)):
        number4.append(
            models.Test.objects.filter(op_unit=name_list3[i]).exclude(
                Q(state="结案") | Q(state="放弃")).count()
        )
    data_dict4 = {'name_list3': name_list3, 'number3': number3, 'number4': number4}

    data_year2 = []
    data_dict5 = {}
    for i in range(2019, d1):
        data_year2.append(i)
    for i in range(len(data_year2)):
        data_dict5[data_year2[i]] = []
        for j in range(1, 13):
            number5 = models.Test.objects.filter(time__year=data_year2[i], time__month=j, state="结案").count()
            number6 = models.Test.objects.filter(time__year=data_year2[i], time__month=j).exclude(state="放弃").count()
            if number6 == 0:
                percentage3 = 0
            else:
                percentage3 = (number5 / number6) * 100
                percentage3 = round(percentage3, 2)
            data_dict5[data_year2[i]].append(percentage3)
            # data_dict5[data_year2[i]].append('{}%'.format(percentage3))
    return render(request, 'login/imk.html', {'data_dict': json.dumps(data_dict), 'data_dict2': json.dumps(data_dict2),
                                              'data_dict3': json.dumps(data_dict3),
                                              'data_dict4': json.dumps(data_dict4),
                                              'data_dict5': json.dumps(data_dict5)})


def imm(request):
    return render(request, 'login/imm.html')


def imn(request):
    return render(request, 'login/imn.html')


def imo(request):
    return render(request, 'login/imo.html')


def imp(request):
    return render(request, 'login/imp.html')


def imq(request):
    return render(request, 'login/imq.html')


def imr(request):
    return render(request, 'login/imr.html')


def ims(request):
    return render(request, 'login/ims.html')


def imt(request):
    return render(request, 'login/imt.html')
