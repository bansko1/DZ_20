from django.urls import path
from blogapp import views

app_name = 'blogapp'

urlpatterns = [
    path('', views.main_view, name='index'),
    path('create/', views.create_post, name='create'),
    path('contact/', views.contact, name='contact'),
    path('ws-list/', views.WsListView.as_view(), name='ws_list'),
    path('word-list/', views.WordListView.as_view(), name='word_list'),
    # path('', views.WordListView.as_view(), name='word_list'),
    path('form-create/', views.ContactView.as_view(), name='form_create')

]
