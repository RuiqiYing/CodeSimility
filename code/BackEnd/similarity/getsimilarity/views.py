from django.http import HttpResponse, JsonResponse

from algorithm.all import algorithmAll
from common import models
from common.models import Answer, QuestionBank


def gethomework(request):
    homeworkid=request.POST.get("homeworkid")
    questionid=request.POST.get("questionid")
    calculation=request.POST.get("calculation")
    # print(homeworkid)
    # print(questionid)
    # print(calculation)
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