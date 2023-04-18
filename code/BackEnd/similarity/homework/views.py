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
from common.models import Homework, HighestSimilarityA, HighestSimilarityB, HighestSimilarityC, SubmitHomework
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


def submittest(request):
    data = json.loads(request.body.decode('utf-8'))
    # print(data)
    userid=data.get('userid')
    questionnum=data.get('questionnum')
    homeworkid=data.get('homeworkid')
    print(userid)
    print(questionnum)
    print(homeworkid)
    return HttpResponse("fuwyseftewgf")

def submit(request): #包含type为1 2 3的一次提交

    data = json.loads(request.body.decode('utf-8'))
    # print(data)
    userid=data.get('userid')
    questionnum=data.get('questionnum')
    homeworkid=data.get('homeworkid')
    dic = data.get('data')
    dataselect=""
    #提交作业表
    SubmitHomework.objects.create(userid=userid,homeworkid=homeworkid,questionnum=questionnum)

    #提交作业表
    for i in dic:  #提交中的一题
        high=[0,0,0]
        useriddic=["","",""]
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
            if questiontype != "1":
                temp = models.Answer.objects.get(userid=userid,questionid=questionid,question=question,answer=answer,homeworkid=homeworkid)
                ansida=temp.ansid
                HighestSimilarityA.objects.create(userida=userid, useridb="null",ansid=ansida,similarity=0.00 , homeworkid=homeworkid)
                HighestSimilarityB.objects.create(userida=userid, useridb="null", ansid=ansida, similarity=0.00, homeworkid=homeworkid)
                HighestSimilarityC.objects.create(userida=userid, useridb="null", ansid=ansida, similarity=0.00, homeworkid=homeworkid)
        else:#不是第一个
            if questiontype=="1":#如果是选择题，存进去
                Answer.objects.create(userid=userid, questionid=questionid, question=question, answer=answer,
                                      questiontype=questiontype, highsimilarityA=0.00, highsimilarityB=0.00,
                                      highsimilarityC=0.00, questionnum=questionnum, homeworkid=homeworkid)

                dataselect+=answer
            else:
                for i in qs:#遍历本次作业中所有题id相同
                    ansid=i.get("ansid")
                    temp = models.Answer.objects.get(ansid=ansid)
                    tempa = models.HighestSimilarityA.objects.get(ansid=ansid)
                    tempb = models.HighestSimilarityB.objects.get(ansid=ansid)
                    tempc = models.HighestSimilarityC.objects.get(ansid=ansid)
                    data1 = algorithmAll(i["answer"], answer)
                    if (i.get("highsimilarityA") < data1[0]):
                        temp.highsimilarityA = data1[0]
                        tempa.similarity = data1[0]
                        tempa.useridb=userid
                    if (i.get("highsimilarityB") < data1[1]):
                        temp.highsimilarityB = data1[1]
                        tempb.similarity = data1[1]
                        tempb.useridb = userid
                    if (i.get("highsimilarityC") < data1[2]):
                        temp.highsimilarityC = data1[2]
                        tempc.similarity = data1[2]
                        tempc.useridb = userid
                    temp.save()
                    tempa.save()
                    tempb.save()
                    tempc.save()
                    if high[0] < data1[0]:
                        high[0] = data1[0]
                        useriddic[0]=i.get("userid")
                    if high[1] < data1[1]:
                        high[1] = data1[1]
                        useriddic[1] = i.get("userid")
                    if high[2] < data1[2]:
                        high[2] = data1[2]
                        useriddic[2] = i.get("userid")
                Answer.objects.create(userid=userid, questionid=questionid, question=question, answer=answer,
                                          questiontype=questiontype, highsimilarityA=high[0], highsimilarityB=high[1],
                                          highsimilarityC=high[2], questionnum=questionnum, homeworkid=homeworkid)
                temp = models.Answer.objects.get(userid=userid, questionid=questionid, question=question, answer=answer,
                                                 homeworkid=homeworkid)
                ansida = temp.ansid
                HighestSimilarityA.objects.create(userida=userid, useridb=useriddic[0], ansid=ansida, similarity=high[0], homeworkid=homeworkid)
                HighestSimilarityB.objects.create(userida=userid, useridb=useriddic[1], ansid=ansida, similarity=high[1], homeworkid=homeworkid)
                HighestSimilarityC.objects.create(userida=userid, useridb=useriddic[2], ansid=ansida, similarity=high[2], homeworkid=homeworkid)
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
        temp = models.Answer.objects.get(userid=userid, homeworkid=homeworkid,selecttype="1")
        ansida = temp.ansid
        HighestSimilarityA.objects.create(userida=userid, useridb="null", ansid=ansida, similarity=0.00, homeworkid=homeworkid)
        HighestSimilarityB.objects.create(userida=userid, useridb="null", ansid=ansida, similarity=0.00, homeworkid=homeworkid)
        HighestSimilarityC.objects.create(userida=userid, useridb="null", ansid=ansida, similarity=0.00, homeworkid=homeworkid)
    else:
        useriddic=["","",""]
        for i in qs:
            ansid = i.get("ansid")
            temp = models.Answer.objects.get(ansid=ansid)
            tempa = models.HighestSimilarityA.objects.get(ansid=ansid)
            tempb = models.HighestSimilarityB.objects.get(ansid=ansid)
            tempc = models.HighestSimilarityC.objects.get(ansid=ansid)
            data1 = algorithmSelect(i["answer"], dataselect)
            if (i.get("highsimilarityA") < data1[0]):
                temp.highsimilarityA = data1[0]
                tempa.similarity = data1[0]
                tempa.useridb = userid
            if (i.get("highsimilarityB") < data1[1]):
                temp.highsimilarityB = data1[1]
                tempb.similarity = data1[1]
                tempb.useridb = userid
            if (i.get("highsimilarityC") < data1[2]):
                temp.highsimilarityC = data1[2]
                tempc.similarity = data1[2]
                tempc.useridb = userid
            temp.save()
            tempa.save()
            tempb.save()
            tempc.save()
            if high[0] < data1[0]:
                high[0] = data1[0]
                useriddic[0] = i.get("userid")
            if high[1] < data1[1]:
                high[1] = data1[1]
                useriddic[1] = i.get("userid")
            if high[2] < data1[2]:
                high[2] = data1[2]
                useriddic[2] = i.get("userid")
        Answer.objects.create(userid=userid, questionid="0", question="作业id" + homeworkid + "的选择题",
                                  answer=dataselect,
                                  questiontype="1", highsimilarityA=high[0], highsimilarityB=high[1],
                                  highsimilarityC=high[2], questionnum=questionnum, homeworkid=homeworkid,
                                  selecttype="1")
        temp = models.Answer.objects.get(userid=userid, homeworkid=homeworkid, selecttype="1")
        ansida = temp.ansid
        HighestSimilarityA.objects.create(userida=userid, useridb=useriddic[0], ansid=ansida, similarity=high[0], homeworkid=homeworkid)
        HighestSimilarityB.objects.create(userida=userid, useridb=useriddic[1], ansid=ansida, similarity=high[1], homeworkid=homeworkid)
        HighestSimilarityC.objects.create(userida=userid, useridb=useriddic[2], ansid=ansida, similarity=high[2], homeworkid=homeworkid)

    return HttpResponse('成功')

def submitcode(request):
    userid=request.POST.get("userid")
    questionnum=request.POST.get("questionnum")
    homeworkid=request.POST.get("homeworkid")
    questionid=request.POST.get("questionid")
    questiontype = request.POST.get('questiontype')
    received_file = request.FILES.get("file")
    filename = os.path.join(MEDIA_ROOT, received_file.name)
    saveFile(received_file, filename)
    content=readFile(filename)
    print(readFile(filename))
    qs = Answer.objects.values()
    qs = qs.filter(questionid=questionid, homeworkid=homeworkid)
    os.remove(MEDIA_ROOT+received_file.name)
    high = [0, 0, 0]
    question= models.QuestionBank.objects.get(questionid=questionid).question
    if qs.count() == 0:
        Answer.objects.create(userid=userid, questionid=questionid, question=question, answer=content,
                              questiontype=questiontype, highsimilarityA=0.00, highsimilarityB=0.00,
                              highsimilarityC=0.00, questionnum=questionnum, homeworkid=homeworkid)
        temp = models.Answer.objects.get(userid=userid, questionid=questionid, question=question, answer=content,
                                         homeworkid=homeworkid)
        ansida = temp.ansid
        HighestSimilarityA.objects.create(userida=userid, useridb="null", ansid=ansida, similarity=0.00, homeworkid=homeworkid)
        HighestSimilarityB.objects.create(userida=userid, useridb="null", ansid=ansida, similarity=0.00, homeworkid=homeworkid)
        HighestSimilarityC.objects.create(userida=userid, useridb="null", ansid=ansida, similarity=0.00, homeworkid=homeworkid)
    else:
        useriddic=["","",""]
        for i in qs:
            ansid = i.get("ansid")
            temp = models.Answer.objects.get(ansid=ansid)
            tempa = models.HighestSimilarityA.objects.get(ansid=ansid)
            tempb = models.HighestSimilarityB.objects.get(ansid=ansid)
            tempc = models.HighestSimilarityC.objects.get(ansid=ansid)
            # print(i["answer"])
            # print(content)

            data1 = algorithmAll(i["answer"], content)
            if (i.get("highsimilarityA") < data1[0]):
                temp.highsimilarityA = data1[0]
                tempa.similarity = data1[0]
                tempa.useridb = userid
            if (i.get("highsimilarityB") < data1[1]):
                temp.highsimilarityB = data1[1]
                tempb.similarity = data1[1]
                tempb.useridb = userid
            if (i.get("highsimilarityC") < data1[2]):
                temp.highsimilarityC = data1[2]
                tempc.similarity = data1[2]
                tempc.useridb = userid
            temp.save()
            tempa.save()
            tempb.save()
            tempc.save()
            if high[0] < data1[0]:
                high[0] = data1[0]
                useriddic[0] = i.get("userid")
            if high[1] < data1[1]:
                high[1] = data1[1]
                useriddic[1] = i.get("userid")
            if high[2] < data1[2]:
                high[2] = data1[2]
                useriddic[2] = i.get("userid")

        Answer.objects.create(userid=userid, questionid=questionid, question=question, answer=content,
                              questiontype=questiontype, highsimilarityA=high[0], highsimilarityB=high[1],
                              highsimilarityC=high[2], questionnum=questionnum, homeworkid=homeworkid)
        temp = models.Answer.objects.get(userid=userid, questionid=questionid, question=question, answer=content)
        ansida = temp.ansid
        HighestSimilarityA.objects.create(userida=userid, useridb=useriddic[0], ansid=ansida, similarity=high[0], homeworkid=homeworkid)
        HighestSimilarityB.objects.create(userida=userid, useridb=useriddic[1], ansid=ansida, similarity=high[1], homeworkid=homeworkid)
        HighestSimilarityC.objects.create(userida=userid, useridb=useriddic[2], ansid=ansida, similarity=high[2], homeworkid=homeworkid)

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


def testcode( request):
    userid = request.POST.get("userid")
    questionid=request.POST.get("questionid")
    received_file = request.FILES.get("file")
    filename = os.path.join(MEDIA_ROOT, received_file.name)
    saveFile(received_file, filename)
    content = readFile(filename)
    print(content)
    print(userid)
    print("isleghfliuewh"+questionid)
    return HttpResponse("chg")

def checksubmit(request):
    userid = request.POST.get("userid")
    homeworkid=request.POST.get("homeworkid")
    try:
        user = models.SubmitHomework.objects.get(userid=userid,homeworkid=homeworkid)
        return HttpResponse("1")#有的话返回1，代表不能再做
    except:
        return HttpResponse("0")

def getsubmitlist(request):
    homeworkid = request.POST.get("homeworkid")
    qs = SubmitHomework.objects.values()
    qs = qs.filter(homeworkid=homeworkid)
    data=[]
    for i in qs:
        data.append(i)
    for i in data:
        simi = HighestSimilarityC.objects.values()
        simi = simi.filter(homeworkid=homeworkid, userida=i["userid"])
        a = 0
        all = 0
        for j in simi:
            all = all + 1
            if (j["similarity"] == 1):
                a = a + 1
        similarityq = a / all
        axis = {"similarity": round(similarityq,4)}
        # axis = {"similarity": a}
        i.update(axis)
    data.sort(key = lambda x:x["similarity"])
    data.reverse()
    return JsonResponse({"ret": 0, "data":data}, json_dumps_params={'ensure_ascii': False},)


def getHomeworkSimilarity(request):
    homeworkid=request.POST.get("homeworkid")
    questionnum=request.POST.get("questionnum")
    tempQ=QuestionBank.objects.values()
    temp1=tempQ.filter(questionnum=questionnum)
    homeworklen=1
    for i in temp1:
        if (i["questiontype"]!="1"):
            homeworklen+=1
    simi = HighestSimilarityC.objects.values()
    simi = simi.filter(homeworkid=homeworkid)
    if(len(simi)==0):
        return HttpResponse("还没有同学提交")
    else:
        jsondata={}
        sub=SubmitHomework.objects.values()
        sub=sub.filter(homeworkid=homeworkid)
        for i in sub:
            jsondata[i["userid"]]=0
        for i in simi:
            if(i["similarity"]==1):
                jsondata[i["userida"]]+=1
        for i in sub:
            jsondata[i["userid"]] = round(jsondata[i["userid"]]/homeworklen,4)
        res = sorted(jsondata.items(), key=lambda jsondata: jsondata[1])
        print(res)
        highsim=res[res.__len__()-1][1]
        highid=res[res.__len__()-1][0]
        lowsim=res[0][1]
        lowid=res[0][0]
        jsonquestion={}
        questiondata=["选择题"]
        for j in temp1:
            if(j["questiontype"]!="1"):
                questiondata.append(j["questionid"])
        qs=Answer.objects.values()
        qs=qs.filter(homeworkid=homeworkid)
        for i in questiondata:
            jsonquestion[str(i)]=[]
        for i in qs:
            if(i["questiontype"]!="1"):
                if(i["highsimilarityC"]==1):
                    p=simi.filter(ansid=i["ansid"])
                    jsontemp={}
                    jsontemp["userid"]=p[0]["userida"]
                    jsonquestion[str(i["questionid"])].append(jsontemp)
            if(i["selecttype"]=="1"):
                if (i["highsimilarityC"] == 1):
                    p=simi.filter(ansid=i["ansid"])
                    jsontemp = {}
                    jsontemp["userid"] = p[0]["userida"]
                    jsonquestion["选择题"].append(jsontemp)
        # print(jsonquestion)
        lenlist=[]
        namelist=[]
        for i in jsonquestion.values():
           lenlist.append(len(i))
        for i in jsonquestion.keys():
            namelist.append(i)
        res = sorted(jsonquestion.items(), key=lambda jsonquestion: len(jsonquestion[1]),reverse=True)

    return JsonResponse({"ret": 0, "highsim":highsim,"highid":highid,"lowsim":lowsim,"lowid":lowid,"jsondata":jsonquestion,"lenlist":lenlist,"namelist":namelist,"sortlist":res}, json_dumps_params={'ensure_ascii': False},)


def checkAnswer(request):
    homeworkid=request.POST.get("homeworkid")
    userid = request.POST.get("userid")
    qs = Answer.objects.values()
    qs = qs.filter(homeworkid=homeworkid,userid=userid)
    data = []
    for i in qs:
        if(i["selecttype"]!='1'):
            data.append(i)
    data.sort(key = lambda x:int(x["questionid"]))
    return JsonResponse({'data': data}, json_dumps_params={'ensure_ascii': False}, )

