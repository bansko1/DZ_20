from django.urls import path, include
from blogapp import views

app_name = 'blogapp'

urlpatterns = [
    path('contact/', views.ContView.as_view(), name='contact'),
    path('', views.WordListView.as_view(), name='word_list'),
    path('form-create/', views.ContactView.as_view(), name='form_create'),
    path('word-detail/<int:pk>/', views.WordDetailView.as_view(), name='word_detail'),
    path('word-create/', views.WordCreateView.as_view(), name='word_create'),
    path('word-delete/<int:pk>/', views.WordDeleteView.as_view(), name='word_delete'),
    path('area-list/', views.AreaListView.as_view(), name='area_list'),
    path('form/', views.vac_create, name='form'),
    path('word-skill/<int:id>/', views.word_skill, name='word_skill'),
    path('word-area/<int:id>/', views.word_area, name='word_area'),
    path('vac-list/<int:id>/', views.vac_word_area, name='vac_list'),
    path('search-result/', views.SearchResultView.as_view(), name='search_result'),
]
