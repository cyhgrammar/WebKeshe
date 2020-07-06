from django.db.models import F
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse  # 功能函数返回json数据
from django.template import loader
from django.http import HttpResponseRedirect  # 重定向
from .models import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt  # 令牌保护
import json  # python对象转json
from django.core import serializers  # 将json数据进行序列化
import qrcode  # 用于二维码的生成
from io import BytesIO  # 用于临时的数据流传输
from django.contrib.auth.decorators import login_required  # 登录才可以使用的方法
from django.contrib.auth import *  # 用户认证系统
from django.contrib.auth.models import User
import datetime


# Create your views here.

# todo:登录+主页

def load1(request):
    logout(request)  # 清空session
    return render(request, 'wage/login.html')


@csrf_exempt
def login_check(request):
    if request.method == 'GET':
        render(request, 'wage/login.html')
    username = request.POST.get('usr', '')
    password = request.POST.get('psd', '')
    user1 = authenticate(username=username, password=password)
    if user1:
        login(request, user1)
        return render(request, 'wage/main.html')
    else:
        return HttpResponse('用户名或密码错误')


@login_required
def index(request):  # 测试用，不能直接进
    list1 = []
    for i in StaffInfo.objects.all().values('E_id'):
        list1.append(i['E_id'])
    return render(request, 'wage/main.html',{'DropList':json.dumps(list1)})

@login_required
def IndexSeek(request):
    if request.method == 'GET':
        return render(request, 'wage/main.html')
    try:
        list1 = StaffInfo.objects.filter(E_id = request.POST.get('province',''))
        list2 = SalaryGrant.objects.filter(E_id = request.POST.get('province',''))
        list3 = CheckRecord.objects.filter(E_id = request.POST.get('province',''))
        return render(request,'wage/main.html',{'data1':list1,'mes1':list2,'mes2':list3})
    except:
        return HttpResponse("输入错误")



# todo:人事管理

@login_required
def AddStaff(request):
    # 加载部门
    list1 = []
    for i in DepartmentList.objects.values('DName'):  # 遍历出来字典
        list1.append(i['DName'])  # 将字典值装入列表
    list2 = []
    list3 = []
    for j in range(len(list1)):
        for k in PositionList.objects.filter(PforDname=list1[j]):  # 查部门相同的职位 返回集合
            list2.append(k.PName)
        list3.append(list2)
        list2 = []
    return render(request, 'wage/AddStaff.html', {'Depart': json.dumps(list1), 'Posi': json.dumps(list3)})


@csrf_exempt
@login_required
def AddStaffDeal(request):
    if request.method == 'GET':
        render(request, 'wage/AddStaff.html')
    staff0 = StaffInfo(Name=request.POST.get('Name', ''), Sex=request.POST.get('Sex', ''),
                       Birth=request.POST.get('Birth', ''), Age=25, Department=request.POST.get('province', ''),
                       Position=request.POST.get('city', ''), Phone=request.POST.get('Phone', ''),
                       Mail=request.POST.get('Mail', ''))
    date1 = datetime.date.today() - datetime.datetime.strptime(staff0.Birth,'%Y-%m-%d').date()  # str -> datetime -> date
    Age0 = date1.days / 365
    staff0.Age = int(Age0)  # 生成年龄
    print(StaffInfo.objects.filter(E_id=staff0.E_id))
    print(staff0.E_id)  # 部门人数加一
    Depart0 = DepartmentList.objects.get(DName=staff0.Department)
    Depart0.DNum = Depart0.DNum+1
    Depart0.save()
    staff0.save()  # 保存后生成E_id
    list1 = []
    for i in PositionList.objects.filter(PforDname=request.POST.get('province', ''),PName=request.POST.get('city', '')):  # 需要获取所在职位的工资
        list1.append(i.Salary)
    staff1 = StaffInfo.objects.get(E_id=staff0.E_id)# 实例化父表对象才可以级联
    Salary1 = BasicSalary(E_id=staff1, Name=staff0.Name, Salary=list1[0], Insurance=400, AbsentDay=60)# 创建工资基本表
    Salary1.save()
    user0 = 'YG' + str(staff0.E_id)  # 登录名
    Account0 = user(WUser=user0, Password='123456', E_id=staff0.E_id, UserTag=1)
    Account0.save()
    return HttpResponse('添加职员成功')

@login_required
def StaffShow(request):
    list1 = StaffInfo.objects.all()
    list2 = []
    for i in StaffInfo.objects.all().values('E_id'):
        list2.append(i['E_id'])
    list3 = []
    for i in DepartmentList.objects.values('DName'):  # 遍历出来字典
        list3.append(i['DName'])  # 将字典值装入列表
    list4 = []
    list5 = []
    for j in range(len(list3)):
        for k in PositionList.objects.filter(PforDname=list3[j]):  # 查部门相同的职位 返回集合
            list4.append(k.PName)
        list5.append(list4)
        list4 = []

    return render(request, 'wage/StaffShow.html', {'data1': list1,'DropList':json.dumps(list2),'Depart': json.dumps(list3), 'Posi': json.dumps(list5)})


@login_required
def StaffStat(request):
    list1 = []
    list2 = []
    for i in DepartmentList.objects.all():
        list1.append(i.DName)
        list2.append(i.DNum)
    list3 = []
    Man0 = len(StaffInfo.objects.filter(Sex = '男'))
    Woman0 = len(StaffInfo.objects.filter(Sex = '女'))
    list3.append({'value':Woman0,'name':'女'})
    list3.append({'value':Man0,'name':'男'})
    return render(request, 'wage/StaffStat.html',{'mes1':json.dumps(list1),'mes2':json.dumps(list2),'mes3':json.dumps(list3)})


@login_required
def UpdateStaff(request):
    if not StaffInfo.objects.filter(E_id = request.POST.get('StaffID',''),Department= request.POST.get('province','')):
        if not StaffInfo.objects.filter(E_id = request.POST.get('StaffID',''),Department= request.POST.get('province',''),Position = request.POST.get('city','')):
            DepartmentList.objects.filter(DName =StaffInfo.objects.get(E_id = request.POST.get('StaffID',''))).update(DNum = F('DNum')-1)
            DepartmentList.objects.filter(DName =request.POST.get('province','')).update(DNum = F('DNum')+1)
            Money = PositionList.objects.get(PName =request.POST.get('city',''),PforDname = request.POST.get('province','')).Salary
            StaffInfo.objects.filter(E_id=request.POST.get('StaffID', '')).update(Department= request.POST.get('province',''),Position=request.POST.get('city', ''))
            BasicSalary.objects.filter(E_id=request.POST.get('StaffID', '')).update(Salary=Money)
            print(1)
            return HttpResponse('更新成功')
        else:
            return HttpResponse('已经有了')
    else:
        Money = PositionList.objects.get(PName=request.POST.get('city', ''),PforDname = request.POST.get('province','')).Salary
        StaffInfo.objects.filter(E_id = request.POST.get('StaffID','')).update(Position = request.POST.get('city',''),)
        BasicSalary.objects.filter(E_id = request.POST.get('StaffID','')).update(Salary=Money)
        print(2)
        return HttpResponse('更新成功')



# todo:工资
@login_required
def SalaryFactor(request):
    list1 = BasicSalary.objects.all()
    list2 = []
    for i in StaffInfo.objects.all().values('E_id'):
        list2.append(i['E_id'])
    return render(request, 'wage/SalaryFactor.html', {'mes1': list1,'DropList':json.dumps(list2)})

@login_required
def UpdBasicSalary(request):
    try:
        BasicSalary.objects.filter(E_id=request.POST.get('province','')).update(Insurance=request.POST.get('insurance0',''),AbsentDay=request.POST.get('absentDay',''))
        return HttpResponse('更新成功')
    except:
        return HttpResponse('超过资金上限')


@login_required
def SalaryPut(request):
    list1 = []
    if request.method == 'GET':
        list1 = SalaryGrant.objects.all()
    else:
        print(SalaryGrant.objects.filter(E_id = int(request.POST.get('province', ''))))
        StartTime = datetime.datetime.strptime(request.POST.get('StartDate', ''), '%Y-%m-%d').date()
        if len(request.POST.get('province', '')) != 0 :
            list1 = SalaryGrant.objects.filter(E_id = int(request.POST.get('province', '')),GrantTime__gte = StartTime)
            print(request.POST.get('province', ''))
        else:
            list1 = SalaryGrant.objects.filter(GrantTime__gte = StartTime)
    list2 = []
    for i in StaffInfo.objects.all().values('E_id'):
        list2.append(i['E_id'])
    if not list1:
        return HttpResponse("无查询结果")
    else:
        return render(request, 'wage/SalaryGrant.html', {'mes1': list1,'DropList':json.dumps(list2)})



@login_required
def SalaryPutDeal(request):
    num0 = request.POST.get('numofday','')
    num1 = int(num0)
    if num1<5 or num1>25:
        return HttpResponse('请输入5—25之间的整数')
    try:
        for i in BasicSalary.objects.all():
            time1 = datetime.date.today()
            time2 = time1 - datetime.timedelta(days=30)
            StartTime = time2
            print(StartTime)
            CheckNum =CheckRecord.objects.filter(CheckTime__gte=StartTime,CheckTime__lte=time1,E_id = i.E_id).count()
            print(CheckNum)
            FaKuan=0
            TiCheng = 0
            if CheckNum<= num1:
                FaKuan = (num1-CheckNum)*i.AbsentDay
                print('fakuan')
                print(FaKuan)
            else:
                TiCheng = (CheckNum-num1)*i.AbsentDay
                print('tic')
                print(TiCheng)
            print(i.Insurance+i.Salary+TiCheng - FaKuan)
            Money0 = i.Insurance+i.Salary+TiCheng - FaKuan
            print(Money0)
            sala0 = SalaryGrant(E_id=i.E_id,Name=i.Name,Salary = i.Salary,Insurance = i.Insurance, Penalty = FaKuan,Royalty =TiCheng,Money=Money0)
            sala0.save()

        return HttpResponse('工资发放成功')
    except:
        return HttpResponse('发生未知错误')


@login_required
def SalaryStat(request):
    list1 = []
    list2 = []
    for i in StaffInfo.objects.all():
        list1.append(i.Name)
        sala0 = 0
        for j in SalaryGrant.objects.filter(E_id=i.E_id):
            sala0 += float(j.Money)
        list2.append(sala0)
    list3 = []
    list4 = []
    for i in DepartmentList.objects.all():
        list3.append(i.DName)
        Money0 = 0
        for j in StaffInfo.objects.filter(Department = i.DName):
            for k in SalaryGrant.objects.filter(E_id = j.E_id):
                Money0+=float(k.Money)
        list4.append(Money0)

    list5 = []
    for l in range(len(list3)):
        list5.append({'value': list4[l], 'name': list3[l]})
    print(list5)
    return render(request, 'wage/SalaryStat.html',{'mes1':json.dumps(list1),'mes2': json.dumps(list2),'mes3':json.dumps(list5),'mes4':json.dumps(list3)})


# todo:考勤
@csrf_exempt
@login_required
def CheckList(request):
    list1 = []
    if request.method == 'GET':
        list1 = CheckRecord.objects.all()
    else:
        StartTime = datetime.datetime.strptime(request.POST.get('StartDate',''), '%Y-%m-%d').date()
        list1 = CheckRecord.objects.filter(CheckTime__gte = StartTime)
    if not list1:
        return HttpResponse('无查询结果')
    num0  = CheckRecord.objects.filter(CheckTime=datetime.date.today()).count()
    num1 = int((num0/StaffInfo.objects.all().count())*100)
    list2=[]
    list2.append({'value': num1, 'name': '当天考勤率'})
    print(list2)
    return render(request, 'wage/CheckList.html', {'mes1': list1,'mes2':json.dumps(list2)})


# todo:个人界面
def QianDao(request):
    return render(request,'wage/QianDao.html')

def QianDaoDeal(request):
    if request.method == 'GET':
        return render(request, 'wage/QianDao.html')
    if user.objects.filter(WUser=request.POST.get('usr',''),Password=request.POST.get('psd','')):
        E_id0 = user.objects.get(WUser=request.POST.get('usr','')).E_id
        staff1 = StaffInfo.objects.get(E_id=E_id0)
        Check0 = CheckRecord(E_id =staff1,CheckTime = timezone.now())
        Check0.save()
        return HttpResponse('签到成功')
    else:
        return HttpResponse('密码或账户错误')

# todo:部门职位
@login_required
def Department(request):
    list1 = DepartmentList.objects.all()
    list2 = []
    for i in DepartmentList.objects.values('DName'):  # 遍历出来字典
        list2.append(i['DName'])  # 将字典值装入列表
    return render(request, 'wage/Department.html', {'mes1': list1,'DropList':list2})


@login_required
def DepartAdd(request):
    try:
        if not DepartmentList.objects.filter(DName = request.POST.get('deofName','')):
            Depart0 = DepartmentList(DName = request.POST.get('deofName',''),DDescribe=request.POST.get('deofName',''),DNum=0)
            Depart0.save()
            return HttpResponse('部门添加成功')
        else:
            return HttpResponse('添加的部门已经存在')
    except:
        return HttpResponse('部门名称过长')


@login_required
def DepartUpd(request):
    try:
        DepartmentList.objects.filter(DName =request.POST.get('Depart0','')).update(DName = request.POST.get('deofName',''),DDescribe=request.POST.get('describe',''))
        StaffInfo.objects.filter(Department =request.POST.get('Depart0','')).update(Department = request.POST.get('deofName',''))
        return HttpResponse('部门更新成功')
    except:
        return HttpResponse('输入部门不存在或与已存在部门重名')


@login_required
def Position(request):
    list1 = PositionList.objects.all()
    list2 = []
    for i in PositionList.objects.all().values('id'):
        list2.append(i['id'])
    list3 = []
    for i in DepartmentList.objects.all().values('DName'):
        list3.append(i['DName'])
    return render(request, 'wage/Position.html', {'mes1': list1,'DepartList':json.dumps(list3),'DropList':json.dumps(list2)})


@login_required
def PosiAdd(request):
    try:
        if not PositionList.objects.filter(PName = request.POST.get('poofName',''),PforDname=request.POST.get('Depart0','')):
            Depart1 = DepartmentList.objects.get(DName = request.POST.get('Depart0',''))
            posi0 = PositionList(PName =request.POST.get('poofName',''),Salary = request.POST.get('basicwage',''),PforDname=Depart1)
            posi0.save()
            return HttpResponse('添加职位成功')
        else:
            return HttpResponse('职位已存在')
    except:
        return HttpResponse('职位名称过长')


@csrf_exempt
@login_required
def PosiDel(request):
    try:
        print(request.POST.get('Dro1',''))
        posi0=PositionList.objects.get(id = request.POST.get('Dro1',''))
        print(posi0.PforDname)
        if not StaffInfo.objects.filter(Department = posi0.PforDname,Position = posi0.PName):
            PositionList.objects.filter(id = posi0.id).delete()
            return HttpResponse('删除职位成功')
        else:
            return HttpResponse('将该职位职员安排到其他职位后才可删除')
    except:
        return HttpResponse('未知错误')



# todo:账号管理
@login_required
def StaffAccounts(request):
    list1 = user.objects.all()
    list3 = []
    for i in StaffInfo.objects.all().values('E_id'):
        list3.append(i['E_id'])

    return render(request, 'wage/StaffAccounts.html', {'mes1': list1,'mes2':23,'DropList':json.dumps(list3)})

@login_required
def UpdAccounts(request):
    if user.objects.filter(WUser=request.POST.get('WUser','')):
        user.objects.filter(WUser=request.POST.get('WUser','')).update(Password = request.POST.get('psd',''))
        return HttpResponse('修改成功')
    else:
        return HttpResponse('无此用户')


@login_required
def DelAccounts(request):
    try:
        user.objects.filter(E_id=request.POST.get('province', '')).delete()
        return HttpResponse('删除成功')
    except:
        return render(request,'wage/error404.html')

@login_required
def AlterPassword(request):
    return render(request, 'wage/AlterPassword.html')


@csrf_exempt
@login_required
def AlterPasswordDetail(request):
    print(request.POST)
    user = request.user
    if request.method == 'POST':
        old_psd = request.POST.get('oldpassword', '')
        new_psd = request.POST.get('password', '')
        repeat_psd = request.POST.get('confirmpassword', '')
    if user.check_password(old_psd):
        if new_psd != repeat_psd:
            return HttpResponse("密码不一致")
        else:
            user.set_password(new_psd)
            user.save()
            return redirect(reverse("wage:cyh"))
    else:
        return HttpResponse('旧密码输入错误')


# todo:测试
def test1(request):
    img = qrcode.make('http://www.jxiou.com/')  # 传入网站计算出二维码图片字节数据
    buf = BytesIO()  # 创建一个BytesIO临时保存生成图片数据
    img.save(buf)  # 将图片字节数据放到BytesIO临时保存
    image_stream = buf.getvalue()  # 在BytesIO临时保存拿出数据
    response = HttpResponse(image_stream, content_type="image/jpg")  # 将二维码数据返回到页面
    return response


def test2(request):
    start_time = datetime.date(2020, 7, 1)
    list1 = CheckRecord.objects.filter(CheckTime__gte = start_time )
    print(len(list1))
    return render(request, 'wage/test1.html',{'mes1':list1})


def test3(request):
    return render(request, 'wage/test1.html')


# todo:错误
def error404(request):
    return render(request, 'wage/error404.html')
