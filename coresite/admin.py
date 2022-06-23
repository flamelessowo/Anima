from coresite.models import Genre, SubGenre, Anime, Studio, Banner, Review, Player, Video, AnimeUserFollowed, \
    UserAnimeRating
from django.contrib import admin

admin.site.site_title = "flameless's administration"
admin.site.site_header = "flameless Administration"

admin.site.register(Genre)
admin.site.register(SubGenre)
admin.site.register(Anime)
admin.site.register(Studio)
admin.site.register(Banner)
admin.site.register(Review)
admin.site.register(Player)
admin.site.register(AnimeUserFollowed)
admin.site.register(Video)
admin.site.register(UserAnimeRating)

