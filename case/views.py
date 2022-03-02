# from urllib import response
from django.shortcuts import redirect, render
from matplotlib.pyplot import title
from .models import Case, Category
from user.models import City
from .forms import CreateCaseForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.paginator import Paginator
from .utils import search_cases, get_page_objects,page_num
# Create your views here.


def cases(request):
    county_id, category_id = 0, 0
    search = ''
    categorys = Category.objects.all()
    countys = City.objects.all()

    category_id = request.COOKIES.get('category_id', 0)
    county_id = request.COOKIES.get('county_id', 0)
    search = request.COOKIES.get('search', '')

    category_id = eval(category_id) if type(category_id) == str else 0
    county_id = eval(county_id) if type(county_id) == str else 0

    if request.method == 'GET':
        page = request.GET.get('page')
        cases = search_cases(category_id, county_id, search)

    if request.method == 'POST':
        # 這邊get 到的是前端網頁select 的name
        # 轉換成數值讓前端網頁程式可以進行數值比對
        category_id = eval(request.POST.get('category')
                           ) if request.POST.get('category') else 0
        county_id = eval(request.POST.get('county')
                         ) if request.POST.get('county') else 0
        search = request.POST.get('search')

    cases = search_cases(category_id, county_id, search)
    
    page_obj = get_page_objects(cases, page, page_num)
    context = {'categorys': categorys,
                'countys': countys, 'category_id': category_id, 'county_id': county_id, 'search': search ,
                'page_obj': page_obj, 'cases_length':len(cases)}

    return render(request, './case/cases.html', context = context)


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
