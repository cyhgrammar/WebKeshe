from django.urls import path
from . import views

app_name = 'wage'  # 为 URL名称添加命名空间
urlpatterns = [
    # 模糊的放在下面
    # 个人页面
    path('QianDao/Deal/',views.QianDaoDeal,name='QianDaoDeal'),
    path('QianDao/', views.QianDao, name='QianDao'),
    # 账号管理
    path('StaffAccounts/Upd/', views.UpdAccounts, name='UpdAccounts'),
    path('StaffAccounts/Del/', views.DelAccounts, name='DelAccounts'),
    path('StaffAccounts/', views.StaffAccounts, name='Accounts'),
    path('AlterPassword/Change/', views.AlterPasswordDetail, name='AlterPasswordDetail'),
    path('AlterPassword/', views.AlterPassword, name='AlterPassword'),
    # 考勤
    path('CheckList/', views.CheckList, name='CheckList'),
    # 部门管理
    path('Department/Add/', views.DepartAdd, name='DepartAdd'),
    path('Department/Upd/', views.DepartUpd, name='DepartUpd'),
    path('Department/', views.Department, name='Department'),
    path('Position/Del/', views.PosiDel, name='PositionDel'),
    path('Position/Add/', views.PosiAdd, name='PositionAdd'),
    path('Position/', views.Position, name='Position'),
    # 工资
    path('SalaryFactor/', views.SalaryFactor, name='SalaryFactor'),
    path('SalaryFactor/Deal/', views.SalaryPutDeal, name='SalaryPutDeal'),#工资发放
    path('SalaryFactor/Upd/', views.UpdBasicSalary, name='UpdSalaryFactor'),
    path('SalaryPut/', views.SalaryPut, name='SalaryPut'),
    path('SalaryStat/', views.SalaryStat, name='SalaryStat'),
    # 人事管理
    path('AddStaff/', views.AddStaff, name='AddStaff'),
    path('AddStaffDeal/', views.AddStaffDeal, name='AddStaffDeal'),
    path('StaffShow/Upd/', views.UpdateStaff,name='StaffUpd'),
    path('StaffShow/', views.StaffShow, name='StaffShow'),
    path('StaffStat/', views.StaffStat, name='StaffStat'),
    # 测试
    path('test1/<int:question_id>/', views.test3, name='qwe'),
    path('test1/', views.test2, name='dfd'),
    # 错误
    path('404/', views.error404, name='error'),
    # 登录
    path('index/seek/', views.IndexSeek, name='indexseek'),
    path('index/', views.index, name='index'),
    path('login/', views.login_check, name='login'),
    path('', views.load1, name='cyh'),

]
