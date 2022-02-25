from urllib import response
from django.shortcuts import redirect, render
from .models import Case
from .forms import CreateCaseForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.


def cases(request):
    cases = Case.objects.all()
    return render(request, './case/cases.html', {'cases': cases})


@login_required(login_url='login')
def create_case(request):
    if request.method == 'GET':
        form = CreateCaseForm()

    if request.method == 'POST':
        form = CreateCaseForm(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            # 設定擁有者
            case.owner = request.user
            case.save()
            # 資料表裡若有多對多關聯 要另外撰寫儲存(save_m2m 無法在變數使用 只能直接使用form來執行)
            form.save_m2m()

            return redirect('cases')
    return render(request, './case/create-case.html', {'form': form})


def case_detail(request, id):
    case = Case.objects.get(id=id)
    case.view += 1
    case.save()

    # 設立cookie 儲存網頁變數
    response = render(request, './case/case-detail.html', {'case': case})
    # cookie 以key:value形式存在 函式('key','value')
    response.set_cookie('page', 'case')

    return response


@login_required(login_url='login')
def delete_case(request, id):
    page = request.COOKIES.get('page')
    case = Case.objects.get(id=id)
    if request.method == 'POST':
        if request.POST.get('confirm'):
            case.delete()
            if page == 'case':
                return redirect('cases')
        # 為了讓選擇取消可以回到原本的case只能多寫這邊因為需要原來的id 而樓上因為刪除了直接導回首頁所以不用id
        if request.POST.get('cancel'):
            if page == 'case':
                return redirect('case-detail', id=case.id)
        # 由於這邊需要先LOGIN才能進來所以進來了request就會有user的值所以可以直接取出user.id
        return redirect('profile', request.user.id)

        # if request.GET.get('cancel'):
        #     return redirect('profile', request.user.id)
    return render(request, './case/delete-case.html', {'case': case})


@login_required(login_url='login')
def update_case(request, id):
    page = request.COOKIES.get('page')
    case = Case.objects.get(id=id)
    if request.method == 'GET':
        # instance = XX  : 將XX裡的內容填充進來 (這函式很重要!!)
        form = CreateCaseForm(instance=case)
    if request.method == 'POST':
        if request.POST.get('confirm'):
            case.updatedon = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            form = CreateCaseForm(request.POST, instance=case)
            if form.is_valid():
                form.save()
                # 修改似乎不影響多對多關聯的儲存 但若儲存不了還是要加上試試看
                # form.save_m2m()
        # 辨識cookies
        if page == 'case':
            return redirect('case-detail', case.id)
        return redirect('profile', request.user.id)
    return render(request, './case/update-case.html', {'form': form, 'page': page})
