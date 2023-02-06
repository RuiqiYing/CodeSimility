# -*-coding:utf-8 -*-
import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from common import models
from common.models import Course


def creat(request):
    coursename = request.POST.get('coursename')
    classname = request.POST.get('classname')
    userid = request.POST.get('userid')
    cTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        course = models.Course.objects.get(coursename=coursename,classname=classname)
        return HttpResponse('该教学班已存在')
    except:
        Course.objects.create(coursename=coursename, classname=classname, userid=userid, ctime=cTime,
                            )

        return HttpResponse('创建成功')

def list(request):
    userId = request.POST.get("userid")
    qs = Course.objects.values()
    qs = qs.filter(userid=userId)
    data=[]
    for i in qs:
        data.append(i)
    return JsonResponse({'ret': 0, 'data': data},json_dumps_params={'ensure_ascii': False},)

def delete(request):
    courseid=request.POST.get("courseid")
    data = Course.objects.get(courseid=courseid)
    data.delete()
    return HttpResponse('删除成功')
