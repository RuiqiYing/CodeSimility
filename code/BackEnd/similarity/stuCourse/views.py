from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from common import models
from common.models import Joincourse, QuestionBank


def joinCourse(request):
    userid=request.POST.get('userid')
    courseid=request.POST.get('courseid')
    try:
        course = models.Joincourse.objects.get(courseid=courseid,userid=userid)
        return HttpResponse("你已加入该课程")
    except:
        try:
            course = models.Course.objects.get(courseid=courseid)
            name = course.coursename
            classname=course.classname
            Joincourse.objects.create(userid=userid, courseid=courseid, coursename=name,classname=classname)
            return HttpResponse("加入成功")
        except:
            return HttpResponse("课程不存在，检查课程ID")

def viewStuCourse(request):
    userid = request.POST.get('userid')
    qs = Joincourse.objects.values()
    qs = qs.filter(userid=userid)
    data = []
    for i in qs:
        data.append(i)
    return JsonResponse({'ret': 0, 'data': data},json_dumps_params={'ensure_ascii': False},)

def getquestionlist(request):
    questionnum=request.POST.get('questionnum')
    qs = QuestionBank.objects.values()
    qs = qs.filter(questionnum=questionnum)
    data = []
    for i in qs:
        data.append(i)
    return JsonResponse({'data': data},json_dumps_params={'ensure_ascii': False},)