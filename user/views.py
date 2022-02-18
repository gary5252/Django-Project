from email import message
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from sympy import Not
from .models import Profile
from .forms import ProfileForm
# Create your views here.


def user_login(request):
    username, password, message = '', '', ''
    if request.method == 'POST':
        # username = request.POST.get('username')
        username = request.POST['username']
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        # print(user)

        if user:
            login(request, user)  # request.user
            # return render(request, './case/cases.html')
            return redirect('cases')

        # 帳號，密碼錯誤
        # filter 多數篩選用函式     username=username  資料表欄位username = 表單輸入進來的username
        if Profile.objects.filter(username=username).exists():
            message = '密碼錯誤'
        else:
            message = '帳號錯誤'

        # print(username, password)

    return render(request, './user/login.html', {'username': username, 'password': password, 'message': message})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('login')


def user_register(request):
    # 先寫入 GET 的情況，因為剛進入網站預設是 GET
    form = ProfileForm()
    if request.method == 'POST':
        # print(request.POST)
        # 接收到 POST 傳遞來的資料
        form = ProfileForm(request.POST)

        # is_valid() 是有效的
        if form.is_valid():
            #  commit = False 先儲存但不確認
            user = form.save(commit=False)
            # user.username = user.username.lower()
            user.save()

            # 註冊完直接使用輸入的資料登入並導回首頁
            login(request, user)  # request.user
            return redirect('cases')

    return render(request, './user/register.html', {'form': form})


def profile(request, id):
    # XX.objects.all() 全部轉物件  XX.objects.get() 單一搜尋  另還有filter見上面
    user = Profile.objects.get(id=id)
    return render(request, './user/profile.html', {'user': user})
