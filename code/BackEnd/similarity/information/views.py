from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from common import models


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

    return HttpResponse("chhg")