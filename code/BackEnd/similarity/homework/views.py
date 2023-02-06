import datetime
import json
import os

from django.conf.global_settings import MEDIA_ROOT
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from common import models
from common.models import Homework
from common.models import QuestionBank,Answer


def creat(request):
    homeworkname = request.POST.get('homeworkname')
    courseid = request.POST.get('courseid')
    questionnum=request.POST.get('questionnum')
    cTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    Homework.objects.create(homeworkname=homeworkname, courseid=courseid, ctime=cTime ,questionnum=questionnum)

    return HttpResponse('创建成功')

def list(request):
    courseid = request.POST.get("courseid")
    qs = Homework.objects.values()
    qs = qs.filter(courseid=courseid)
    data=[]
    for i in qs:
        data.append(i)
    return JsonResponse({'ret': 0, 'data': data},json_dumps_params={'ensure_ascii': False},)

def delete(request):
    homeworkid=request.POST.get("homeworkid")
    data = Homework.objects.get(homeworkid=homeworkid)
    data.delete()
    return HttpResponse('删除成功')

def gethomework(request):
    questionnum=request.POST.get("questionnum")
    qs = QuestionBank.objects.values()
    qs = qs.filter(questionnum=questionnum)
    data=[]
    for i in qs:
        data.append(i)
    return JsonResponse({'ret': 0, 'length':data.__len__(), 'data': data}, json_dumps_params={'ensure_ascii': False}, )


def submit(request):
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    userid=data.get('userid')
    questionnum=data.get('questionnum')
    homeworkid=data.get('homeworkid')
    dic = data.get('data')
    for i in dic:
        questionid=i.get('questionid')
        question=i.get('question')
        answer=i.get("answer")
        questiontype=i.get('questiontype')
        # print(questiontype)
        # print(questionid)
        # print(question)
        # print(answer)
        # print(userid)
        # print(questionnum)
        # print(homeworkid)
        qs = Answer.objects.values()
        qs = qs.filter(questionid=questionid,homeworkid=homeworkid)
        if qs.count()==0:
            Answer.objects.create(userid=userid,questionid=questionid,question=question,answer=answer,questiontype=questiontype,highsimilarityA='0.00',highsimilarityB='0.00',highsimilarityC='0.00',questionnum=questionnum,homeworkid=homeworkid)
    return HttpResponse('成功')

def submitcode(request):
    userid=request.POST.get("userid")
    questionnum=request.POST.get("questionnum")
    homeworkid=request.POST.get("homeworkid")
    questionid=request.POST.get("questionid")
    question=request.POST.get("question")
    questiontype = request.POST.get('questiontype')
    # print("user:"+userid)
    received_file = request.FILES.get("file")
    filename = os.path.join(MEDIA_ROOT, received_file.name)
    saveFile(received_file, filename)
    content=readFile(filename)
    print(readFile(filename))
    qs = Answer.objects.values()
    qs = qs.filter(questionid=questionid, homeworkid=homeworkid)
    os.remove(MEDIA_ROOT+received_file.name)
    if qs.count() == 0:
        Answer.objects.create(userid=userid, questionid=questionid, question=question, answer=content,
                              questiontype=questiontype, highsimilarityA='0.00', highsimilarityB='0.00',
                              highsimilarityC='0.00', questionnum=questionnum, homeworkid=homeworkid)


    return HttpResponse('成功')


def saveFile(received_file, filename):
    with open(filename, 'wb')as f:
        f.write(received_file.read())

# 读取上传的文件内容，并返回
def readFile(filename):
    with open(filename,'r')as f:
        content = f.read()
    return content