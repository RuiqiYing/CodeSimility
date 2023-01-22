import random

from django.shortcuts import render,HttpResponse

# Create your views here.
from app01 import models


def index(request,username,password,):
    # person = models.Person()
    #
    # # 设置属性
    # person.p_name = "王" + str(random.randint(1, 100))
    # person.p_age = random.randint(1, 100)
    # person.p_sex = random.randint(0, 1)
    #
    # # 保存数据
    # person.save()
    # b=models.Person.objects.all()
    # print(b)
    return HttpResponse("欢迎使用")