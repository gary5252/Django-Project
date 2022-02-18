from pyexpat import model
from attr import field, fields
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# 建立表單


class ProfileForm(UserCreationForm):
    # 基礎設定
    class Meta:
        # 繼承哪個資料表的欄位
        model = Profile
        # 需要輸入者輸入那些資料    password1,2 必須配合使用的官方 form 對應寫死
        fields = ['username', 'email', 'password1',
                  'password2', 'city', 'respondent']
