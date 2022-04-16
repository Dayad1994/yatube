from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    # Страница создания поста
    path('new/', views.new_post, name='new_post'),
    # комментарии
    path('<str:username>/<int:post_id>/comment/', views.add_comment,
         name='add_comment'),
    # Просмотр и редактирование записи
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
