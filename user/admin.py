from django.contrib import admin
from .models import City, Respondent, Profile
# Register your models here.

# 將新增的資料表註冊進資料庫
admin.site.register(City)
admin.site.register(Respondent)
admin.site.register(Profile)
