from coresite.views import IndexView, anime_detail_view, category_view, categories_view, player_view
from django.urls import path
from Anima import settings
from django.conf.urls.static import static

app_name = 'Anima'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('anime/categories/', categories_view, name='categories'),
    path('anime/<slug>/player/<int:episode>/', player_view, name='player'),
    path('anime/<slug>/', anime_detail_view, name='anime'),
    path('anime/category/<slug>', category_view, name='category')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
