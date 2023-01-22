import datetime


from django.http import HttpResponse, JsonResponse

from common import models
from common.models import User



def register(request):
    userId = request.POST.get('userid')
    userName = request.POST.get('username')
    passWord = request.POST.get('password')
    role=request.POST.get('role')
    information="介绍一下自己吧"
    cTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    User.objects.create(username=userName,password=passWord,userid=userId,role=role,ctime=cTime,information=information)

    return JsonResponse({'ret': 0})

def login(request):
    userId = request.POST.get('userid')
    passWord = request.POST.get('password')
    role = request.POST.get('role')
    # print(userId)
    # print(passWord)
    # print(role)
    corr_id = User.objects.filter(userid=userId).first()
    try:
        user = models.User.objects.get(userid=userId)
        if user.password == passWord:
            if role=="0":
                print("111")
                return JsonResponse({'ret': 0,'data':"22" })
            else:
                print("111")
                return JsonResponse({'ret': 0,'data':"22" })
        else:
            return HttpResponse('密码错误')
    except:
        return HttpResponse("用户名不存在！")


def pwd_update(request):
    userid=request.POST.get('userid')
    new_pwd=request.POST.get('password')
    try:
        user = models.User.objects.get(userid=userid)
        if user.password == new_pwd:
            return HttpResponse("两次密码不能相同")
        else:
            user.password=new_pwd
            user.save()
            return HttpResponse("修改成功")
    except:
        return HttpResponse("用户名不存在！")



