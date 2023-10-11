from django.urls import path
from blogapp import views

app_name = 'blogapp'

urlpatterns = [
    path('contact/', views.ContView.as_view(), name='contact'),
    path('ws-list/', views.WsListView.as_view(), name='ws_list'),
    path('', views.WordListView.as_view(), name='word_list'),
    path('form-create/', views.ContactView.as_view(), name='form_create')
]
