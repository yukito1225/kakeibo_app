from django.urls import path
from . import views
from kakeibo import views

app_name = 'kakeibo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:now_page>', views.index, name='index'),
    path('<int:now_page>', views.show_line_grahp, name='kakeibo_line'),
    path('post', views.post, name='post'),
    path('save', views.save, name='save'),
    path('set_record_number/', views.set_record_number, name='set_record_number'),
    path('set_order/', views.set_order, name='set_order'),
    path('insert', views.insert, name='insert'),
    path('category_insert', views.category_insert, name='category_insert'),
    path('update/<int:num>', views.update ,name='update'),
    path('line/', views.show_line_grahp, name='kakeibo_line'),
]