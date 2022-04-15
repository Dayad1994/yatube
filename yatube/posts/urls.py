from django.urls import path

from . import views

urlpatterns = [
    # Страница создания поста
    path('new/', views.new_post, name='new_post'),
    # Просмотр записи
    path('<str:username>/<int:post_id>/edit/', views.post_edit,
         name='post_edit'),
    path('<str:username>/<int:post_id>/', views.post_view, name='post'),
    # Профайл пользователя
    path('<str:username>/', views.profile, name='profile'),
    # Страница группы
    path('group/<slug:slug>/', views.group_posts, name='group'),
    # Главная страница
    path('', views.index, name='index'),
]
