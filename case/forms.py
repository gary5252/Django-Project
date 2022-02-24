from pyexpat import model
from attr import fields
from django.forms import ModelForm
from .models import Case


class CreateCaseForm(ModelForm):  # class表單名稱(使用表單原型)
    # 基礎設定
    class Meta:
        # 繼承哪個資料表的欄位
        model = Case
        # exclude 為不需要輸入者輸入的欄位
        exclude = ['owner']
        fields = ['title', 'category', 'state', 'description', 'contact', 'amount',
                  'respondent', 'skill', 'period', 'mode']
        # fields = '__all__'  全部欄位顯示(會排除 exclude 欄位)
