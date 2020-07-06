from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(user)
admin.site.register(StaffInfo)
admin.site.register(BasicSalary)
admin.site.register(SalaryGrant)
admin.site.register(CheckRecord)
admin.site.register(DepartmentList)
admin.site.register(PositionList)
