from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from common import models
from common.models import Answer, HighestSimilarityA, HighestSimilarityB, HighestSimilarityC


def getusername(request):
    userid = request.POST.get("userid")
    user = models.User.objects.get(userid=userid)
    username=user.username
    return HttpResponse(username)

def getallinfor(request):
    userid = request.POST.get("userid")
    user = models.User.objects.get(userid=userid)
    return  JsonResponse({"ret": 0, "username": user.username, "information": user.information,"ctime":user.ctime})


def changeinformation(request):
    userid = request.POST.get("userid")
    username=request.POST.get("username")
    information=request.POST.get("information")
    user = models.User.objects.get(userid=userid)
    user.username = username
    user.information=information
    user.save()
    return HttpResponse("修改成功")



def gethomeworkname(request):
    userid = request.POST.get("userid")
    qs = Answer.objects.values()
    qs = qs.filter(userid=userid)
    data=[]
    homeworkid=[]
    for i in qs:
        flag=0
        id=i["homeworkid"]
        for i in homeworkid:
            if(i==id):
                flag=1
        if(flag==0):
            homeworkid.append(id)
            print(id)
            homework= models.Homework.objects.get(homeworkid=id)
            data.append(homework.homeworkname)
    return JsonResponse({"ret":0,"data":data,"homeworkid":homeworkid})

def getstusimilarity(request):
    homeworkid=request.POST.get("homeworkid")
    userid=request.POST.get("userid")
    calculation = request.POST.get("calculation")
    ans=Answer.objects.values()
    data=[]
    similaritydata=[]
    if(calculation=="1"):
        qs = HighestSimilarityA.objects.values()
        qs = qs.filter(userida=userid, homeworkid=homeworkid)
        for i in qs:
            ansid=i["ansid"]
            temp=ans.filter(ansid=ansid)
            if(temp[0]["selecttype"]=="1"):
                data.insert(0,"选择题")
            else:
                data.append(temp[0]["questionid"])
    if (calculation == "2"):
        qs = HighestSimilarityB.objects.values()
        qs = qs.filter(userida=userid, homeworkid=homeworkid)
        for i in qs:
            ansid = i["ansid"]
            temp = ans.filter(ansid=ansid)
            if (temp[0]["selecttype"] == "1"):
                data.insert(0, "选择题")
            else:
                data.append(temp[0]["questionid"])
    if (calculation == "3"):
        qs = HighestSimilarityC.objects.values()
        qs = qs.filter(userida=userid, homeworkid=homeworkid)
        for i in qs:
            ansid = i["ansid"]
            temp = ans.filter(ansid=ansid)
            if (temp[0]["selecttype"] == "1"):
                data.insert(0, "选择题")
            else:
                data.append(temp[0]["questionid"])
    return JsonResponse({"data":data})