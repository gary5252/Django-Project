from operator import mod
from pickle import TRUE
from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import SET_NULL

# Create your models here.

# Primary Key 不用寫   models 會自動產生
# 新增資料表 class : 資料表名稱 (繼承自何模型)  欄位名稱 = models.資料類型(資料限制:長度，重複性，空值允許)


class City(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    # 藉由 Meta 調整一些 options   ordering 排序
    class Meta:
        ordering = ['id']

    # 欄位顯示
    def __str__(self):
        return f'{self.name}-{self.createdon}'


class Respondent(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False)
    createdon = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

# AbstractUser --> Django 本身的 User 虛擬模型


class Profile(AbstractUser):
    point = models.IntegerField(default=0)
    certification = models.BooleanField(default=False)
    city = models.ForeignKey(City, on_delete=SET_NULL, null=True)
    respondent = models.ForeignKey(Respondent, on_delete=SET_NULL, null=True)

    def __str__(self):
        return f'{self.username}-{self.point}-{self.certification}'
