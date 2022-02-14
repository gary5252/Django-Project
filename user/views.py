from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from sympy import Not
# Create your views here.


def user_login(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        username = request.POST['username']
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)  # request.user
            # print(user)
            # return render(request, './case/cases.html')
            return redirect('cases')
        else:
            print('登入失敗')

        # print(username, password)

    return render(request, './user/login.html')
