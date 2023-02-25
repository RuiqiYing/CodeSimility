import datetime
import json
import os
import string

from django.conf.global_settings import MEDIA_ROOT
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.
from algorithm.all import algorithmAll, algorithmSelect
from algorithm.cosine_similarity import CosineSimilarity
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


def submit(request): #包含type为1 2 3的一次提交
    data = json.loads(request.body.decode('utf-8'))
    print(data)
    userid=data.get('userid')
    questionnum=data.get('questionnum')
    homeworkid=data.get('homeworkid')
    dic = data.get('data')
    dataselect=""
    for i in dic:  #提交中的一题
        high=[0,0,0]
        questionid=i.get('questionid')
        question=i.get('question')
        answer=i.get("answer")
        questiontype=i.get('questiontype')
        # print("answer:"+answer)
        qs = Answer.objects.values()
        qs = qs.filter(questionid=questionid,homeworkid=homeworkid)#选择题目，看是否存在
        if qs.count()==0 : #不存在即第一个交作业，无论什么，都直接存进去，跳过相似度比较
            if questiontype == "1":
                dataselect += answer
            Answer.objects.create(userid=userid,questionid=questionid,question=question,answer=answer,questiontype=questiontype,highsimilarityA=0.00,highsimilarityB=0.00,highsimilarityC=0.00,questionnum=questionnum,homeworkid=homeworkid)
        else:#不是第一个
            if questiontype=="1":#如果是选择题，存进去
                Answer.objects.create(userid=userid, questionid=questionid, question=question, answer=answer,
                                      questiontype=questiontype, highsimilarityA=0.00, highsimilarityB=0.00,
                                      highsimilarityC=0.00, questionnum=questionnum, homeworkid=homeworkid)

                dataselect+=answer
            else:
                for i in qs:
                    ansid=i.get("ansid")
                    temp = models.Answer.objects.get(ansid=ansid)
                    data1 = algorithmAll(i["answer"], answer)
                    if (i.get("highsimilarityA") < data1[0]):
                        temp.highsimilarityA = data1[0]
                    if (i.get("highsimilarityB") < data1[1]):
                        temp.highsimilarityB = data1[1]
                    if (i.get("highsimilarityC") < data1[2]):
                        temp.highsimilarityC = data1[2]
                    temp.save()
                    if high[0] < data1[0]:
                        high[0] = data1[0]
                    if high[1] < data1[1]:
                        high[1] = data1[1]
                    if high[2] < data1[2]:
                        high[2] = data1[2]
                Answer.objects.create(userid=userid, questionid=questionid, question=question, answer=answer,
                                          questiontype=questiontype, highsimilarityA=high[0], highsimilarityB=high[1],
                                          highsimilarityC=high[2], questionnum=questionnum, homeworkid=homeworkid)

                # print(data1)
                # print()
    #处理选择题
    high=[0,0,0]
    qs = Answer.objects.values()
    qs = qs.filter( homeworkid=homeworkid,selecttype="1")  # 选择题目，看是否存在
    if qs.count()==0:
        Answer.objects.create(userid=userid, questionid="0", question="作业id"+homeworkid+"的选择题", answer=dataselect,
                              questiontype="1", highsimilarityA=0.00, highsimilarityB=0.00,
                              highsimilarityC=0.00, questionnum=questionnum, homeworkid=homeworkid,selecttype="1")
    else:
        for i in qs:
            ansid = i.get("ansid")
            temp = models.Answer.objects.get(ansid=ansid)
            data1 = algorithmSelect(i["answer"], dataselect)
            if (i.get("highsimilarityA") < data1[0]):
                temp.highsimilarityA = data1[0]
            if (i.get("highsimilarityB") < data1[1]):
                temp.highsimilarityB = data1[1]
            if (i.get("highsimilarityC") < data1[2]):
                temp.highsimilarityC = data1[2]
            temp.save()
            if high[0] < data1[0]:
                high[0] = data1[0]
            if high[1] < data1[1]:
                high[1] = data1[1]
            if high[2] < data1[2]:
                high[2] = data1[2]
        Answer.objects.create(userid=userid, questionid="0", question="作业id" + homeworkid + "的选择题",
                                  answer=dataselect,
                                  questiontype="1", highsimilarityA=high[0], highsimilarityB=high[1],
                                  highsimilarityC=high[2], questionnum=questionnum, homeworkid=homeworkid,
                                  selecttype="1")

        # print(data1)
        # print()
        # print("处理本次提交中所有的选择题")
    # print(dataselect)

    return HttpResponse('成功')

def submitcode(request):
    userid=request.POST.get("userid")
    questionnum=request.POST.get("questionnum")
    homeworkid=request.POST.get("homeworkid")
    questionid=request.POST.get("questionid")
    question=request.POST.get("question")
    questiontype = request.POST.get('questiontype')
    received_file = request.FILES.get("file")
    filename = os.path.join(MEDIA_ROOT, received_file.name)
    saveFile(received_file, filename)
    content=readFile(filename)
    # print(readFile(filename))
    qs = Answer.objects.values()
    qs = qs.filter(questionid=questionid, homeworkid=homeworkid)
    os.remove(MEDIA_ROOT+received_file.name)
    high = [0, 0, 0]
    if qs.count() == 0:
        Answer.objects.create(userid=userid, questionid=questionid, question=question, answer=content,
                              questiontype=questiontype, highsimilarityA=0.00, highsimilarityB=0.00,
                              highsimilarityC=0.00, questionnum=questionnum, homeworkid=homeworkid)
    else:
        for i in qs:
            ansid = i.get("ansid")
            temp = models.Answer.objects.get(ansid=ansid)
            # print(i["answer"])
            # print(content)
            data1 = algorithmAll(i["answer"], content)
            if (i.get("highsimilarityA") < data1[0]):
                temp.highsimilarityA = data1[0]
            if (i.get("highsimilarityB") < data1[1]):
                temp.highsimilarityB = data1[1]
            if (i.get("highsimilarityC") < data1[2]):
                temp.highsimilarityC = data1[2]
            temp.save()
            if high[0] < data1[0]:
                high[0] = data1[0]
            if high[1] < data1[1]:
                high[1] = data1[1]
            if high[2] < data1[2]:
                high[2] = data1[2]
        Answer.objects.create(userid=userid, questionid=questionid, question=question, answer=content,
                              questiontype=questiontype, highsimilarityA=high[0], highsimilarityB=high[1],
                              highsimilarityC=high[2], questionnum=questionnum, homeworkid=homeworkid)

    return HttpResponse('成功')


def saveFile(received_file, filename):
    with open(filename, 'wb')as f:
        f.write(received_file.read())

# 读取上传的文件内容，并返回
def readFile(filename):
    with open(filename,'r',encoding='UTF-8')as f:
        content = f.read()
    return content


def courseSimilarity(courseid):
    data=[]
    return JsonResponse({"ret": 0, "data":data})
