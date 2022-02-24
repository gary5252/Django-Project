from pyexpat import model
from attr import field, fields
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# 建立表單


class ProfileForm(UserCreationForm):  # class表單名稱(使用表單原型)
    # 基礎設定
    class Meta:
        # 繼承哪個資料表的欄位
        model = Profile
        # fields 為需要輸入者輸入那些資料(exclude 為那些不需要輸入的)    password1,2 必須配合使用的官方 form 對應寫死
        fields = ['username', 'email', 'password1',
                  'password2', 'city', 'respondent']
