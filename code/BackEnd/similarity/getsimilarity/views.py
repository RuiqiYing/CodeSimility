from django.http import HttpResponse, JsonResponse

from algorithm.all import algorithmAll
from common import models
from common.models import Answer, QuestionBank


def gethomework(request):
    homeworkid=request.POST.get("homeworkid")
    questionid=request.POST.get("questionid")
    calculation=request.POST.get("calculation")

    qs = Answer.objects.values()
    qs = qs.filter(homeworkid=homeworkid,questionid=questionid)
    data=[]
    if (calculation=="1"):
        for i in qs:
            data.append(i["highsimilarityA"])
    elif (calculation == "2"):
        for i in qs:
            data.append(i["highsimilarityB"])
    else:
        for i in qs:
            data.append(i["highsimilarityC"])
    print(data)
    return JsonResponse({"ret": 0, "data": data})

def getsum(request):
    questionnum=request.POST.get("questionnum")
    qs = QuestionBank.objects.values()
    qs = qs.filter(questionnum=questionnum)
    data=["选择题"]
    for i in qs:
        if (i["questiontype"]!="1"):
            data.append(i["questionid"])
    return JsonResponse({"ret": 0, "data":data})


def compare(request):
    userid1=request.POST.get("userid1")
    userid2 = request.POST.get("userid2")
    questionid=request.POST.get("questionid")
    algorithm=request.POST.get("algorithm")
    ans1 = models.Answer.objects.get(userid=userid1,questionid=questionid)
    ans2 = models.Answer.objects.get(userid=userid2, questionid=questionid)
    question=ans1.question
    answer1=ans1.answer
    answer2 = ans2.answer
    data=algorithmAll(answer1,answer2)
    similarity=""
    if (algorithm=="1"):
        similarity=data[0]
    elif(algorithm=="2"):
        similarity = data[1]
    elif(algorithm=="3"):
        similarity = data[2]
    return JsonResponse({"ret": 0, "answer1": answer1, "answer2": answer2,"question":question,"similarity":similarity})




def getsimdetail(request):

    #查看一次作业各算法各区间的人数及姓名
    homeworkid=request.POST.get("homeworkid")
    questionid=request.POST.get("questionid")
    calculation=request.POST.get("calculation")
    range=request.POST.get("range")
    qs = Answer.objects.values()
    qs = qs.filter(homeworkid=homeworkid,questionid=questionid)
    data=[]
    stuinfor=[]
    if (calculation=="1"):
        for i in qs:
            if (range == "1"):
                if(i["highsimilarityA"]>=0 and i["highsimilarityA"]<=0.2):
                    data.append(i["highsimilarityA"])
                    stuinfor.append(i["userid"])
            elif (range == "2"):
                if(i["highsimilarityA"]>0.2 and i["highsimilarityA"]<=0.4):
                    data.append(i["highsimilarityA"])
                    stuinfor.append(i["userid"])
            elif (range == "3"):
                if (i["highsimilarityA"] > 0.4 and i["highsimilarityA"] <= 0.6):
                    data.append(i["highsimilarityA"])
                    stuinfor.append(i["userid"])
            elif (range == "4"):
                if (i["highsimilarityA"] > 0.6 and i["highsimilarityA"] <= 0.8):
                    data.append(i["highsimilarityA"])
                    stuinfor.append(i["userid"])
            elif (range == "5"):
                if (i["highsimilarityA"] > 0.8 and i["highsimilarityA"] <=1):
                    data.append(i["highsimilarityA"])
                    stuinfor.append(i["userid"])
    elif (calculation == "2"):
        for i in qs:
            if (range == "1"):
                if (i["highsimilarityB"] > 0 and i["highsimilarityB"] <= 0.2):
                    data.append(i["highsimilarityB"])
                    stuinfor.append(i["userid"])
            elif (range == "2"):
                if (i["highsimilarityB"] > 0.2 and i["highsimilarityB"] <= 0.4):
                    data.append(i["highsimilarityB"])
                    stuinfor.append(i["userid"])
            elif (range == "3"):
                if (i["highsimilarityB"] > 0.4 and i["highsimilarityB"] <= 0.6):
                    data.append(i["highsimilarityB"])
                    stuinfor.append(i["userid"])
            elif (range == "4"):
                if (i["highsimilarityB"] > 0.6 and i["highsimilarityB"] <= 0.8):
                    data.append(i["highsimilarityB"])
                    stuinfor.append(i["userid"])
            elif (range == "5"):
                if (i["highsimilarityB"] > 0.8 and i["highsimilarityB"] <= 1):
                    data.append(i["highsimilarityB"])
                    stuinfor.append(i["userid"])
    else:
        for i in qs:
            if (range == "1"):
                if (i["highsimilarityC"] > 0 and i["highsimilarityC"] <= 0.2):
                    data.append(i["highsimilarityC"])
                    stuinfor.append(i["userid"])
            elif (range == "2"):
                if (i["highsimilarityC"] > 0.2 and i["highsimilarityC"] <= 0.4):
                    data.append(i["highsimilarityC"])
                    stuinfor.append(i["userid"])
            elif (range == "3"):
                if (i["highsimilarityC"] > 0.4 and i["highsimilarityC"] <= 0.6):
                    data.append(i["highsimilarityC"])
                    stuinfor.append(i["userid"])
            elif (range == "4"):
                if (i["highsimilarityC"] > 0.6 and i["highsimilarityC"] <= 0.8):
                    data.append(i["highsimilarityC"])
                    stuinfor.append(i["userid"])
            elif (range == "5"):
                if (i["highsimilarityC"] > 0.8 and i["highsimilarityC"] <= 1):
                    data.append(i["highsimilarityC"])
                    stuinfor.append(i["userid"])

    return JsonResponse({"ret": 0, "data":data ,"stuinfor":stuinfor})


def getstuhomeworksim(request):#得到某同学某次作业相似度
    userid=request.POST.get("userid")
    homeworkid=request.POST.get("homeworkid")
    calculation = request.POST.get("calculation")
    qs = Answer.objects.values()
    qs = qs.filter(homeworkid=homeworkid, userid=userid)
    num = []
    similarity = []
    if (calculation == "1"):
        for i in qs:
            if(i["selecttype"]=='1'):
                num.insert(0,"选择题")
                similarity.insert(0,i["highsimilarityA"])
            elif(i["selecttype"]!='1' and i["questiontype"]!='1'):
                num.append(i["questionid"])
                similarity.append(i["highsimilarityA"])
    elif (calculation == "2"):
        for i in qs:
            if(i["selecttype"]=="1"):
                num.insert(0,"选择题")
                similarity.insert(0,i["highsimilarityB"])
            elif (i["selecttype"] != '1' and i["questiontype"] != '1'):
                num.append(i["questionid"])
                similarity.append(i["highsimilarityB"])
    elif (calculation == "3"):
        for i in qs:
            if(i["selecttype"]=="1"):
                num.insert(0,"选择题")
                similarity.insert(0,i["highsimilarityC"])
            elif (i["selecttype"] != '1' and i["questiontype"] != '1'):
                num.append(i["questionid"])
                similarity.append(i["highsimilarityC"])
    return JsonResponse({"ret": 0, "id":num ,"similarity":similarity})

