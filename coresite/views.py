from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist

from .forms import ReviewForm
from .models import Anime, Banner, Genre, Review, Player, AnimeUserStatus, UserAnimeRating


class IndexView(ListView):
    model = Anime
    template_name = 'index.html'
    context_object_name = 'animes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'banners': Banner.objects.all(),
            'top_views_animes': Anime.objects.all().order_by('-views'),
            'reviews': Review.objects.all(),
            'form': ReviewForm
        })
        return context


# class AnimeDetail(DetailView):
#     models = Anime
#     template_name = 'anime-details.html'
#     slug_url_kwarg = 'slug'
#
#     def get_object(self, queryset=None):
#         slug = self.kwargs.get(self.slug_url_kwarg)
#         anime = get_object_or_404(Anime, slug=slug)
#         return anime
#
#     def get_context_data(self, **kwargs):
#         slug = self.kwargs.get(self.slug_url_kwarg)
#         anime = get_object_or_404(Anime, slug=slug)
#         context = super(AnimeDetail, self).get_context_data(**kwargs)
#         context['reviews'] = Review.objects.filter(anime=anime)
#         return context


def anime_detail_view(request, slug):
    if request.method == 'GET':
        anime = get_object_or_404(Anime, slug=slug)
        form = ReviewForm()
        try:
            status = AnimeUserStatus.objects.get(user=request.user, anime=anime, anime_watched=True)
            if status.graded:
                user_grade = UserAnimeRating.objects.get(user=request.user, anime=anime)
                context = {
                    'anime': anime,
                    'reviews': Review.objects.filter(anime=anime),
                    'form': form,
                    'status': status,
                    'user_grage': user_grade
                }
                return render(request, 'anime-details.html', context)
            context = {
                'anime': anime,
                'reviews': Review.objects.filter(anime=anime),
                'form': form,
                'status': status
            }
            return render(request, 'anime-details.html', context)
        except ObjectDoesNotExist:
            context = {
                'anime': anime,
                'reviews': Review.objects.filter(anime=anime),
                'form': form,
            }
            return render(request, 'anime-details.html', context)
        except TypeError:
            context = {
                'anime': anime,
                'reviews': Review.objects.filter(anime=anime),
                'form': form,
            }
            return render(request, 'anime-details.html', context)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            anime = get_object_or_404(Anime, slug=slug)
            form = ReviewForm({'user': request.user, 'anime': anime, 'text': request.POST['text']})
            if form.is_valid():
                form.save()
                return redirect("Anima:anime", anime.slug)


def categories_view(request):
    queryset = Genre.objects.all()
    first_half = Genre.get_first_half()
    second_half = Genre.get_second_half()
    context = {
        'categories': queryset,
        'first_half': first_half,
        'second_half': second_half
    }
    return render(request, 'categoriesAll.html', context)


def category_view(request, slug):
    genre = Genre.objects.get(slug=slug)
    animes = Anime.objects.filter(categories=genre)
    paginator = Paginator(animes, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'categories.html'
    context = {
        'genre': genre,
        'animes': animes,
        'page_obj': page_obj,
        'reviews': Review.objects.all(),
    }
    return render(request, template, context)


def player_view(request, slug, episode):
    anime = get_object_or_404(Anime, slug=slug)
    player = Player.objects.get(anime=anime)
    context = {
        'anime': anime,
        'player': player
    }
    return render(request, 'anime-watching.html', context)
