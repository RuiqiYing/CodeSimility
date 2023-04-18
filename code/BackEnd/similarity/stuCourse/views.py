from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from algorithm.all import algorithmAll
from common import models
from common.models import Joincourse, QuestionBank, Answer


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
    id1 = request.POST.get("id1")
    id2 = request.POST.get("id2")
    homeworkid = request.POST.get("homeworkid")
    simidata = []
    qs = Answer.objects.values()
    qs = qs.filter(homeworkid=homeworkid, userid=id1)
    qs1 = Answer.objects.values()
    qs1 = qs1.filter(homeworkid=homeworkid, userid=id2)

    qsdic = []
    qsdic1 = []
    for i in qs:
        qsdic.append(i)
    for j in qs1:
        qsdic1.append(j)
    qsdic.sort(key=lambda x: int(x["questionid"]))
    qsdic1.sort(key=lambda x: int(x["questionid"]))
    for i in qsdic:
        if (i["selecttype"] != '1'):
            answer1 = i["answer"]
            qid = i["questionid"]
            for j in qsdic1:
                if (j["questionid"] == qid):
                    answer2 = j["answer"]
                    simidata.append(algorithmAll(answer1, answer2))
    qs = QuestionBank.objects.values()
    qs = qs.filter(questionnum=questionnum)
    data = []
    for i in qs:
        data.append(i)
    return JsonResponse({'data': data,'simidata':simidata},json_dumps_params={'ensure_ascii': False},)