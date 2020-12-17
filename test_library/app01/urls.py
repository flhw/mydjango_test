from django.conf.urls import url
from app01 import views

urlpatterns = [
    url(r'^publisher_list/', views.publisher_list,name='publisher'),
    url(r'^publisher_add/', views.publisher_add),
    url(r'^publisher_del/', views.publisher_del),
    url(r'^publisher_edit/', views.publisher_edit),
    url(r'^book_list/', views.book_list,name='book'),
    url(r'^book_add/', views.book_add,name='book_add'),
    url(r'^book_del/', views.book_del),
    url(r'^book_edit/', views.book_edit),
    url(r'^author_list/', views.author_list,name='author'),
    url(r'^author_add/', views.author_add),
    url(r'^author_del/', views.author_del),
    url(r'^author_edit/', views.author_edit),
]
