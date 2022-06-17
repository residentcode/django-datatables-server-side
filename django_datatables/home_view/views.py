import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from home_view.models import People


def home_view(request):
    if request.method != 'POST':
        return render(request, 'home_view.html')
    order_idx = int(request.POST.get('order[0][column]'))
    order_dir = request.POST.get('order[0][dir]')
    order_col = 'columns[' + str(order_idx) + '][data]'
    order_col_name = request.POST.get(order_col)
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    get_length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')
    if order_dir == 'desc':
        order_col_name = str('-' + order_col_name)
        order_objects = People.objects.all().order_by(order_col_name)
    else:
        order_objects = People.objects.all().order_by(order_col_name)
    # print(dict(request.POST.items()))
    length = order_objects.count()
    records_total = length
    records_filtered = records_total
    paginator = Paginator(order_objects, get_length)

    if search:
        order = People.objects.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(city__icontains=search) |
            Q(gender__icontains=search)
        )
        records_total = order.count()
        records_filtered = records_total
        # After search
        paginator = Paginator(order, get_length)
    page_number = start / get_length + 1
    try:
        object_list = paginator.page(page_number).object_list
    except PageNotAnInteger:
        object_list = paginator.page(1).object_list
    except EmptyPage:
        object_list = paginator.page(1).object_list

    data = [
        {
            'first_name': val.first_name,
            'last_name': val.last_name,
            'email': val.email,
            'city': val.city,
            'gender': val.gender,

        } for val in object_list
    ]

    return JsonResponse({
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'start': page_number,
        'data': data,

    })


def data_tables_json_file(request):
    if request.method != 'POST':
        return render(request, 'home_view.html')
    with open('employee.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    order_idx = int(request.POST.get('order[0][column]'))
    order_dir = request.POST.get('order[0][dir]')
    order_col = 'columns[' + str(order_idx) + '][data]'
    order_col_name = request.POST.get(order_col)
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    get_length = int(request.POST.get('length'))
    search = request.POST.get('search[value]')

    if order_dir == 'desc' and order_col_name:
        data.sort(key=lambda d: d[order_col_name], reverse=True)

    if order_dir == 'asc' and order_col_name:
        sorted(data, key=lambda d: d[order_col_name], reverse=False)

    records_total = len(data)
    records_filtered = len(data)
    paginator = Paginator(data, get_length)

    if search:
        found = list(filter(lambda item:
                            f'{item["first_name"]}{item["last_name"]}{item["email"]}{item["city"]}{item["gender"]}'
                            .lower().find(search.lower()) > -1, data
                            )
                     )

        length = len(found)
        records_total = length
        records_filtered = records_total
        paginator = Paginator(found, get_length)
    page_number = start / get_length + 1
    try:
        object_list = paginator.page(page_number).object_list
    except PageNotAnInteger:
        object_list = paginator.page(1).object_list
    except EmptyPage:
        object_list = paginator.page(1).object_list

    return JsonResponse({
        'draw': draw,
        'recordsTotal': records_total,
        'recordsFiltered': records_filtered,
        'start': page_number,
        'data': object_list,

    })
