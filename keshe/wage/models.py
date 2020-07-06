from django.db import models
import datetime #设置默认日期
from django.utils import timezone #设置默认时间
# Create your models here.
class user(models.Model):
    WUser = models.CharField(max_length=10,primary_key=True,verbose_name='用户名')
    Password = models.CharField(max_length=16,verbose_name='密码')
    E_id = models.IntegerField(verbose_name='用户ID')
    UserTag = models.IntegerField(verbose_name='用户类型')

class StaffInfo(models.Model):
    E_id = models.AutoField(primary_key=True,verbose_name='用户ID')
    Name= models.CharField(max_length=6,verbose_name='姓名')
    Sex = models.CharField(verbose_name='性别',max_length=1)
    Birth= models.DateField(verbose_name='出生日期',default=datetime.date.today())
    Hiredate =  models.DateField(verbose_name='入职日期',default=datetime.date.today())
    Age = models.IntegerField(verbose_name='年龄')
    Department = models.CharField(max_length=10,verbose_name='部门')
    Position = models.CharField(max_length=10,verbose_name='职位')
    Phone = models.CharField(max_length=11,verbose_name='手机号')
    Mail = models.CharField(verbose_name='邮箱',max_length=25)

    def __str__(self):
        return str(self.E_id)

class BasicSalary(models.Model):
    E_id = models.ForeignKey(StaffInfo, on_delete=models.CASCADE, verbose_name='用户ID',primary_key=True)
    Name = models.CharField(max_length=6, verbose_name='姓名')
    Salary = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='基础工资')
    Insurance = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='保险')
    AbsentDay = models.DecimalField(max_digits=6,decimal_places=2,verbose_name='缺勤扣款/天')

    def __str__(self):
        return str(self.E_id) + ' '+ self.Name

class SalaryGrant(models.Model):
    E_id = models.ForeignKey(StaffInfo, on_delete=models.CASCADE, verbose_name='用户ID')
    Name = models.CharField(max_length=6, verbose_name='姓名')
    GrantTime = models.DateTimeField(verbose_name='发放时间',default=timezone.now())
    Salary = models.DecimalField(max_digits=8, decimal_places=2,verbose_name='基础工资')
    Insurance = models.DecimalField(max_digits=8, decimal_places=2,verbose_name='保险')
    Penalty = models.DecimalField(max_digits=8, decimal_places=2,verbose_name='罚款')
    Royalty = models.DecimalField(max_digits=8, decimal_places=2,verbose_name='提成')
    Money = models.DecimalField(max_digits=8, decimal_places=2,verbose_name='最终金额')

    def __str__(self):
        return self.Name + str(self.GrantTime)

class CheckRecord(models.Model):
    E_id = models.ForeignKey(StaffInfo, on_delete=models.CASCADE,verbose_name='用户ID')
    CheckTime = models.DateTimeField(verbose_name='签到时间',default= timezone.now())


class DepartmentList(models.Model):
    DName = models.CharField(max_length=10,verbose_name='部门名称',primary_key=True)
    DDescribe = models.CharField(max_length=30,verbose_name='部门描述')
    DNum = models.IntegerField(verbose_name='部门人数')

    def __str__(self):
        return  self.DName


class PositionList(models.Model):
    PName = models.CharField(max_length=10,verbose_name='职位名称')
    PforDname = models.ForeignKey(DepartmentList,on_delete=models.CASCADE,max_length=10,verbose_name='所属部门')
    Salary = models.DecimalField(max_digits=8, decimal_places=2,verbose_name='基础工资')







