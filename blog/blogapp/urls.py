from django.urls import path
from blogapp import views

app_name = 'blogapp'

urlpatterns = [
    path('contact/', views.ContView.as_view(), name='contact'),
    path('ws-list/', views.WsListView.as_view(), name='ws_list'),
    # path('ws-list/<int:pk>/', views.WsListView.as_view(), name='ws_list'),
    path('', views.WordListView.as_view(), name='word_list'),
    path('form-create/', views.ContactView.as_view(), name='form_create'),
    path('vacancy-list/', views.VacancyListView.as_view(), name='vacancy_list'),
    path('word-detail/<int:pk>/', views.WordDetailView.as_view(), name='word_detail'),
    path('word-create/', views.WordCreateView.as_view(), name='word_create'),
    path('word-delete/<int:pk>/', views.WordDeleteView.as_view(), name='word_delete'),
    path('area-list/', views.AreaListView.as_view(), name='area_list'),
    path('form/', views.word_create, name='form'),
]
