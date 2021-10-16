from django.shortcuts import render, redirect
from .forms import  RecordNumberForm,OrderForm,UpdateForm,KakeiboForm,CategoryInsertForm
from .models import Category, Kakeibo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import calendar
from django.db.models import Sum
from django.views import generic
from datetime import datetime, date
from apscheduler.schedulers.blocking import BlockingScheduler
import sys
from django.db import models
#from apscheduler.schedulers.background import BackgroundScheduler


def index(request, now_page=1):
    if 'record_number' in request.session:
        record_number = request.session['record_number']
    else: 
        record_number = 10

    record_number_form = RecordNumberForm()
    record_number_form.initial = {'record_number': str(record_number)}

    if 'order_option' in request.session:
        order_option = request.session['order_option']
    else:
        order_option = 10

    order_form = OrderForm()
    order_form.initial = {'order_option': str(order_option)}

    if order_option == '1':
        categorys = Kakeibo.objects.all().order_by('date')
    else:
        categorys = Kakeibo.objects.all().order_by('date').reverse()


    page = Paginator(categorys, record_number)
    params = {
        'page': page.get_page(now_page),
        'record_number_form': record_number_form,
        'order_form': order_form,
    }
    return render(request, 'kakeibo/index.html', params)

def post(request):
    post_pks = request.POST.getlist('delete')
    Kakeibo.objects.filter(pk__in=post_pks).delete()
    
    form = KakeiboForm(request.POST, instance=Kakeibo())

    if 'button_3' in request.POST:
        form.save()
        return redirect(to='/kakeibo')

    elif 'button_4' in request.POST:
        form.save()
        return redirect(to='/kakeibo/insert')
    else:
        print(form.errors)

    return redirect('/kakeibo') 

def insert(request):
    form = KakeiboForm()

    params = {
        'KakeiboForm':form,
    }

    return render(request, 'kakeibo/insert.html',params)

def save(request):
    form = CategoryInsertForm(request.POST, instance=Category())

    if 'button_1' in request.POST:
        form.save()
        print("helt")
        return redirect(to='/kakeibo')

    elif 'button_2' in request.POST:
        form.save()
        return redirect(to='/kakeibo/category_insert')
    else:
        print(form.errors)

    

def category_insert(request):
    form = CategoryInsertForm()

    params = {
        'CategoryInsertForm':form,
    }

    return render(request, 'kakeibo/category_insert.html',params)        

def update(request,num):
    #import pdb; pdb.set_trace()
    kakeibo = Kakeibo.objects.get(id=num)
    if request.method == 'POST':
        form = UpdateForm(request.POST,instance=kakeibo)
        form.save()
        return redirect(to='/kakeibo')
    else:
        params = {
            'id':num,
            'form':UpdateForm(instance=kakeibo)
        }

    return render(request, 'kakeibo/update.html',params)


def set_record_number(request):
    request.session['record_number'] = request.POST['record_number']
    return redirect(to='/kakeibo')

def set_order(request):
    request.session['order_option'] = request.POST['order_option']
    return redirect(to='/kakeibo')

def show_line_grahp(request):


    #カテゴリ毎の合計金額を求める
    #まずはカテゴリ名のリストデータを生成する。
    category_list =[]
    #全カテゴリ名をテーブルから取得する。
    category_data = Category.objects.all()
    #ループ処理でカテゴリ名のリストを作成する。
    for item in category_data:
        category_list.append(item.category_name)

    syokuhi_total = Kakeibo.objects.filter(category__category_name=category_list[0]).aggregate(sum=models.Sum('money'))['sum']
    koutuhi_total = Kakeibo.objects.filter(category__category_name=category_list[1]).aggregate(sum=models.Sum('money'))['sum']
    zappi_total = Kakeibo.objects.filter(category__category_name=category_list[2]).aggregate(sum=models.Sum('money'))['sum']
    keihi_total = Kakeibo.objects.filter(category__category_name=category_list[3]).aggregate(sum=models.Sum('money'))['sum']

    #全データ取得
    kakeibo_data = Kakeibo.objects.all()

    category1 = Category.objects.get(id=1)
    category2 = Category.objects.get(id=2)
    category3 = Category.objects.get(id=3)
    category4 = Category.objects.get(id=4)

    #カテゴリリストデータの生成
    category_list =[]
    category_data = Category.objects.all().order_by('-category_name')
    for item in category_data:
        category_list.append(item.category_name)


    #日付ラベルの取得(グラフのｘ軸となるデータ)
    date_list=[]
    for i in kakeibo_data:
        date_list.append((i.date.strftime('%Y/%m/%d')[:7]))

    
    #重複値の除外
    x_label = list(set(date_list))
    x_label.sort(reverse=False)

    

    #月毎＆カテゴリ毎の合計金額データセットの生成
    monthly_sum_data =[]
    for i in range(len(x_label)):
        year,month = x_label[i].split("/")
        month_range = calendar.monthrange(int(year),int(month))[1]
        first_date = year + '-' + month +'-' + '01'
        last_date = year + '-' + month + '-' + str(month_range)
        #１か月分データを取得
        total_of_month = Kakeibo.objects.filter(date__range=(first_date, last_date))
        category_total = total_of_month.values('category').annotate(total_price=Sum('money'))

        
        for j in range(len(category_total)):
            money = category_total[j]['total_price']
            category = Category.objects.get(pk=category_total[j]['category'])
            monthly_sum_data.append([x_label[i], category.category_name,money])

            
        print(monthly_sum_data[1][2])

    #月毎＆カテゴリ毎の合計金額データを生成する。
    #カテゴリが登録されていない月の合計金額は０にセットする。
    #まず、全日付ｘ全カテゴリｘ合計金額「0]のリストを生成する。
    matrix_list =[]
    for item_label in x_label:
        for item_category in category_list:
            matrix_list.append([item_label, item_category, 0])
    
    """
    matrix_listとmonthlysum_dataに対して、「年月+カテゴリ」の
    組み合わせが一致する要素に対してmatrix_listの金額（０円）を
    monthly_sum_dataの金額で上書きする。
    """
    
    for yyyy_mm,category,total in monthly_sum_data:
        for i,data in enumerate(matrix_list):
            if data[0]==yyyy_mm and data[1] ==category:
                matrix_list[i][2] = total

    return render(request, 'kakeibo/kakeibo_line.html',{
        'x_label': x_label,
        'category_list': category_list,
        'matrix_list': matrix_list,
        'kakeibo_data': kakeibo_data,
        'category1':category1,
        'category2':category2,
        'category3':category3,
        'category4':category4,
        'date_list':date_list,
        'syokuhi_total':syokuhi_total,
        'koutuhi_total':koutuhi_total,
        'zappi_total':zappi_total,
        'keihi_total':keihi_total,
         } )
"""

def iphone():
    print('こんにちは')

def start():
   
   Scheduling data update
   Run update function once every 12 seconds
   
   scheduler = BackgroundScheduler()
   
   scheduler.add_job(update, 'interval', seconds=12) # schedule
   scheduler.start()

"""