from django.shortcuts import redirect, render
from .models import Case
from .forms import CreateCaseForm
from django.contrib.auth.decorators import login_required
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
    return render(request, './case/case-detail.html', {'case': case})
