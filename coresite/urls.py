from coresite.views import IndexView, anime_detail_view, category_view, generic_category_view, categories_view, user_page_view, user_edit_view, player_view, add_remove_follow, set_score
from django.urls import path
from Anima import settings
from django.conf.urls.static import static

app_name = 'Anima'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('anime/categories/', categories_view, name='categories'),
    path('anime/<str:name>', generic_category_view, name='generic_category'),
    path('anime/<slug>/', anime_detail_view, name='anime'),
    path('anime/<slug>/player/<int:episode>', player_view, name='player'),
    path('anime/<slug>/follow', add_remove_follow, name='follow'),
    path('anime/<slug>/rating/<int:rating>', set_score, name='score'),
    path('anime/category/<slug>', category_view, name='category'),
    path('user/<str:username>/edit', user_edit_view, name='user_edit'),
    path('user/<str:username>/', user_page_view, name='userpage'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
