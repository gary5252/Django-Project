from django.contrib import admin
from sympy import OmegaPower
from .models import City, Respondent, Profile
from django.contrib.auth.admin import UserAdmin
from .forms import ProfileForm
# Register your models here.

# 將新增的資料表註冊進資料庫
admin.site.register(City)
admin.site.register(Respondent)


class ProfileAdmin(UserAdmin):
    model = Profile
    add_form = ProfileForm
    fieldsets = [
        *UserAdmin.fieldsets,
        [
            'User role',
            {
                'fields': [
                    'point', 'certification', 'city', 'respondent'
                ]
            }
        ]
    ]


admin.site.register(Profile, ProfileAdmin)
