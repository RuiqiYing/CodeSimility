import os

import xlsxwriter as xw

from django.conf.global_settings import MEDIA_ROOT
from django.http import HttpResponse, JsonResponse, FileResponse

from algorithm.all import algorithmAll
from common import models
from common.models import Answer, QuestionBank,SubmitHomework, HighestSimilarityA, HighestSimilarityB, HighestSimilarityC, \
    SubmitHomework


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
    tuijian="算法一"
    if(len(answer2)>80 or len(answer1)>80 ):
        tuijian = "算法二"
    return JsonResponse({"ret": 0, "answer1": answer1, "answer2": answer2,"question":question,"similarity":similarity,"tuijian":tuijian})




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
                if(i["highsimilarityA"]>=0 and i["highsimilarityA"]<0.2):
                    data.append(i["highsimilarityA"])
                    stuinfor.append(i["userid"])
            elif (range == "2"):
                if(i["highsimilarityA"]>=0.2 and i["highsimilarityA"]<0.4):
                    data.append(i["highsimilarityA"])
                    stuinfor.append(i["userid"])
            elif (range == "3"):
                if (i["highsimilarityA"] >= 0.4 and i["highsimilarityA"] < 0.6):
                    data.append(i["highsimilarityA"])
                    stuinfor.append(i["userid"])
            elif (range == "4"):
                if (i["highsimilarityA"] >= 0.6 and i["highsimilarityA"] < 0.8):
                    data.append(i["highsimilarityA"])
                    stuinfor.append(i["userid"])
            elif (range == "5"):
                if (i["highsimilarityA"] >= 0.8 and i["highsimilarityA"] <=1):
                    data.append(i["highsimilarityA"])
                    stuinfor.append(i["userid"])
    elif (calculation == "2"):
        for i in qs:
            if (range == "1"):
                if (i["highsimilarityB"] > 0 and i["highsimilarityB"] < 0.2):
                    data.append(i["highsimilarityB"])
                    stuinfor.append(i["userid"])
            elif (range == "2"):
                if (i["highsimilarityB"] >= 0.2 and i["highsimilarityB"] < 0.4):
                    data.append(i["highsimilarityB"])
                    stuinfor.append(i["userid"])
            elif (range == "3"):
                if (i["highsimilarityB"] >= 0.4 and i["highsimilarityB"] < 0.6):
                    data.append(i["highsimilarityB"])
                    stuinfor.append(i["userid"])
            elif (range == "4"):
                if (i["highsimilarityB"] >= 0.6 and i["highsimilarityB"] < 0.8):
                    data.append(i["highsimilarityB"])
                    stuinfor.append(i["userid"])
            elif (range == "5"):
                if (i["highsimilarityB"] >= 0.8 and i["highsimilarityB"] <= 1):
                    data.append(i["highsimilarityB"])
                    stuinfor.append(i["userid"])
    else:
        for i in qs:
            if (range == "1"):
                if (i["highsimilarityC"] > 0 and i["highsimilarityC"] < 0.2):
                    data.append(i["highsimilarityC"])
                    stuinfor.append(i["userid"])
            elif (range == "2"):
                if (i["highsimilarityC"] >= 0.2 and i["highsimilarityC"] < 0.4):
                    data.append(i["highsimilarityC"])
                    stuinfor.append(i["userid"])
            elif (range == "3"):
                if (i["highsimilarityC"] >= 0.4 and i["highsimilarityC"] < 0.6):
                    data.append(i["highsimilarityC"])
                    stuinfor.append(i["userid"])
            elif (range == "4"):
                if (i["highsimilarityC"] >= 0.6 and i["highsimilarityC"] < 0.8):
                    data.append(i["highsimilarityC"])
                    stuinfor.append(i["userid"])
            elif (range == "5"):
                if (i["highsimilarityC"] >= 0.8 and i["highsimilarityC"] <= 1):
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
    useriddata=[]
    similarity = []
    if (calculation == "1"):
        for i in qs:
            if(i["selecttype"]=='1'):
                num.insert(0,"选择题")
                similarity.insert(0,i["highsimilarityA"])
                useriddata.insert(0,models.HighestSimilarityA.objects.get(ansid=i["ansid"]).useridb)
            elif(i["selecttype"]!='1' and i["questiontype"]!='1'):
                num.append(i["questionid"])
                similarity.append(i["highsimilarityA"])
                useriddata.append( models.HighestSimilarityA.objects.get(ansid=i["ansid"]).useridb)
    elif (calculation == "2"):
        for i in qs:
            if(i["selecttype"]=="1"):
                num.insert(0,"选择题")
                similarity.insert(0,i["highsimilarityB"])
                useriddata.insert(0, models.HighestSimilarityB.objects.get(ansid=i["ansid"]).useridb)
            elif (i["selecttype"] != '1' and i["questiontype"] != '1'):
                num.append(i["questionid"])
                similarity.append(i["highsimilarityB"])
                useriddata.append(models.HighestSimilarityB.objects.get(ansid=i["ansid"]).useridb)

    elif (calculation == "3"):
        for i in qs:
            if(i["selecttype"]=="1"):
                num.insert(0,"选择题")
                similarity.insert(0,i["highsimilarityC"])
                useriddata.insert(0, models.HighestSimilarityC.objects.get(ansid=i["ansid"]).useridb)

            elif (i["selecttype"] != '1' and i["questiontype"] != '1'):
                num.append(i["questionid"])
                similarity.append(i["highsimilarityC"])
                useriddata.append( models.HighestSimilarityC.objects.get(ansid=i["ansid"]).useridb)
    return JsonResponse({"ret": 0, "id":num ,"similarity":similarity,"useriddata":useriddata})



def getfile(request):
    homeworkid=request.POST.get("homeworkid")
    homeworkname = request.POST.get("homeworkname")
    qs = Answer.objects.values()
    qs = qs.filter(homeworkid=homeworkid)
    data=[]
    user=SubmitHomework.objects.values()
    user=user.filter(homeworkid=homeworkid)
    for i in user:
        userid=i["userid"]
        temp=qs.filter(userid=userid)
        tdic=[]
        for i in temp:
            tdic.append(i)
            tdic.sort(key = lambda x:int(x["questionid"]))
        for i in tdic:
            data.append(i)
    print(data)
    fileName = 'filedic/'+homeworkname+'.xlsx'
    xw_toExcel(data, fileName)
    #拿到文件在数据库中存储的位置
    media_file=fileName
    # 拼接文件路径
    filepath = os.path.join(MEDIA_ROOT, media_file)
    #拿到文件的名字（该名字包含了文件的格式）
    print(filepath)
    filename =media_file.split(r'/')[-1]
    file = open(filepath, 'rb')
    response = FileResponse(file)  # 生成文件对象application/msword  application/octet-stream
    response['Content-Type'] = 'application/octet-stream'
    #name.split('.')[0] + '.docx'，
    name = filename
    response['Content-Disposition'] = 'attachment;filename ="%s"' % (
        name.encode('utf-8').decode('ISO-8859-1'))
    return response


def xw_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['学号', '题目id', '题目','答案','相似度1','相似度2','相似度3',]  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(data)):
        insertData = [data[j]["userid"], data[j]["questionid"], data[j]["question"],data[j]["answer"], data[j]["highsimilarityA"], data[j]["highsimilarityB"], data[j]["highsimilarityC"]]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    workbook.close()  # 关闭表
