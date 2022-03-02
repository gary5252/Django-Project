from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Case

page_num = 20

def search_cases(category_id, county_id, search = ''):
    # Q 可以拿來用在 and/or 的多重篩選
        category_q = Q(category_id=category_id)
        # 透過case所屬owner去查找所屬profile裡的city.id 此雙重搜尋要使用雙底線__
        county_q = Q(owner__city_id=county_id)
        # XX__(雙底線)contains = YY : 在XX中是否有包含YY   ( | : or  ,  & : and )
        search_q = Q(title__contains=search) | Q(description__contains=search)

        if category_id and county_id:
            # 多重篩選  \是為了換行加的
            cases = Case.objects.filter(category_q & county_q & search_q) if search else\
                Case.objects.filter(category_q & county_q)
            # cases = Case.objects.filter(category_id=category_id).filter(owner__city_id=county_id)
        elif category_id:
            # filter 多數篩選 篩選出來資料表裡category.id = 網頁前端藉由POST 傳遞回來的category_id
            cases = Case.objects.filter(category_q & search_q) if search else\
                Case.objects.filter(category_q)
        elif county_id:
            cases = Case.objects.filter(county_q & search_q) if search else\
                Case.objects.filter(county_q)
        elif search:
            cases = Case.objects.filter(search_q)
        else:
            cases = Case.objects.all()
        return cases

def get_page_objects(cases, page, page_num):
    paginator = Paginator(cases, page_num)  # Show 25 contacts per page.
    try:
        page_obj = paginator.get_page(page)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)
    return page_obj