import os
from django.db import models
from Anima import settings
from users.models import User

ANIME_TYPES = [
    ('TV', 'TV Series'),
    ('OVA', 'OVA'),
    ('FILM', 'FILM')
]

STATUS = [
    ('Airing', 'Airing'),
    ('Ended', 'Ended')
]

RATINGS = [
    (1, 'Insignificantly'),
    (2, 'Ugly'),
    (3, 'Bad'),
    (4, 'Anyhow'),
    (5, 'Mediocre'),
    (6, 'Not bad'),
    (7, 'Good'),
    (8, 'Great'),
    (9, 'Superb'),
    (10, 'Masterpiece')

]

QUALITIES = [
    ('144p', '144p'),
    ('240p', '240p'),
    ('360p', '360p'),
    ('480p', '480p'),
    ('720p', '720p'),
    ('1080p', '1080p')
]


class Studio(models.Model):
    name = models.CharField(max_length=254, unique=True, null=False)

    class Meta:
        managed = True
        verbose_name = 'Studio'
        verbose_name_plural = 'Studios'
        ordering = ['-name']

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    title = models.CharField(verbose_name='Title', max_length=254, null=False)
    description = models.TextField(max_length=5000, null=False)
    slug = models.SlugField(default='dummy-slug', verbose_name='Slug')
    image = models.ImageField(default='f', upload_to='genre/images')

    # exclude one for styling
    @classmethod
    def get_first_half(cls):
        len_half = len(Genre.objects.all()) / 2
        half = Genre.objects.all()[1:len_half]
        return half

    @classmethod
    def get_second_half(cls):
        len_half = len(Genre.objects.all()) / 2
        half = Genre.objects.all()[len_half:]
        return half

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['-title']


class SubGenre(Genre):
    genre_of = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True, related_name='sub_genre')

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        verbose_name = 'Sub Genre'
        verbose_name_plural = 'Sub Genres'
        ordering = ['-title']


class Anime(models.Model):
    title = models.CharField(verbose_name='Title', max_length=254, null=False)
    description = models.TextField(verbose_name='Description', max_length=5000, null=False)
    categories = models.ManyToManyField(Genre, verbose_name='Categories')
    series = models.PositiveIntegerField(verbose_name='Series', null=False, default=0)
    type = models.CharField(choices=ANIME_TYPES, null=False, max_length=30)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE)
    date_aired = models.DateTimeField(verbose_name='Airing started')
    date_aired_end = models.DateTimeField(verbose_name='Airing ended')
    status = models.CharField(choices=STATUS, null=False, verbose_name='Status', max_length=50)
    rating = models.IntegerField(choices=RATINGS, null=False)
    views = models.PositiveIntegerField(default=0)
    trending = models.BooleanField(default=False)
    popular = models.BooleanField(default=False)
    image = models.ImageField(verbose_name="Image", upload_to='anime/images', default='f')
    slug = models.SlugField(verbose_name='Slug', default='dummy-anime')

    @property
    def get_absolute_image_url(self):
        return "{0}{1}".format(settings.MEDIA_URL, self.image.url)

    @property
    def get_str_genres(self):
        return ''.join(str(genre) + ', ' for genre in self.categories.all())[:-2]

    def __str__(self) -> str:
        return self.title

    class Meta:
        managed = True
        verbose_name = 'Anime'
        verbose_name_plural = 'Animes'
        ordering = ['title', '-rating']


class Banner(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, null=False)
    description = models.TextField(blank=True)
    banner_image = models.ImageField(verbose_name='Banner Image', null=False)

    def __str__(self) -> str:
        return self.anime.title + ' Banner'


class Video(models.Model):
    anime_type = models.CharField(choices=ANIME_TYPES, max_length=15, null=False, blank=True)
    season = models.IntegerField(null=False, blank=True)
    episode = models.IntegerField(null=False, blank=True, default=1)
    caption = models.CharField(max_length=240, null=False)
    quality = models.CharField(choices=QUALITIES, max_length=15, null=False, blank=True)

    def content_file_name(self, filename):
        ext = filename.split('.')[-1]
        if not ext == 'mp4':
            raise Exception("Unsupported format")
        filename = f"{self.caption}_{self.season}_{self.anime_type}_ep{self.episode}_{self.quality}.{ext}"
        if self.anime_type == 'TV':
            return os.path.join(f"uploads/TV/{self.caption}/season_{self.season}", filename)
        return os.path.join('uploads', filename)

    video = models.FileField(upload_to=content_file_name)

    def get_video_path(self):
        return f"uploads/TV/{self.caption}/season_{self.season}"

    def __str__(self):
        return f"{self.caption}, season {self.season}, episode {self.episode}"


class Player(models.Model):
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    videos = models.ManyToManyField(Video)
    season = models.IntegerField(null=False, blank=True)

    def __str__(self):
        return f"Player: {self.anime}, Season {self.season}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, default=2)
    text = models.TextField(max_length=1000, blank=False, null=False)
    time = models.DateTimeField(auto_now=True)


class AnimeUserStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    graded = models.BooleanField(default=False, verbose_name='Graded')
    anime_watched = models.BooleanField(default=False, verbose_name='Watched')
    anime_will_watch = models.BooleanField(default=False, verbose_name='Will Watch')
    anime_abandoned = models.BooleanField(default=False, verbose_name='Abandoned')
    anime_loved = models.BooleanField(default=False, verbose_name='Loved')

    def __str__(self):
        return f"{self.user.username if self.user.username else self.user.email} status on {self.anime.title}"

    class Meta:
        unique_together = ['user', 'anime']

    # TODO override save() to allow only one true in bool fields


class UserAnimeRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATINGS)

    def __str__(self):
        return f"{self.user} - {self.rating} on {self.anime}"
