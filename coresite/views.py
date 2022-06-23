from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls.base import reverse
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model

from .forms import ReviewForm
from users.forms import UserForm
from .models import Anime, Banner, Genre, Review, UserAnimeRating, AnimeUserFollowed


class IndexView(ListView):
    model = Anime
    template_name = 'index.html'
    context_object_name = 'animes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'banners': Banner.objects.all(),
            'top_views_animes': Anime.objects.all().order_by('-views'),
            'announced': Anime.objects.all().filter(status='Announced')[:4],
            'recently_added': Anime.objects.all().order_by('-date_added')[:6],
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
        animes = Anime.objects.filter(categories__in=[anime.categories.first()]).exclude(id=anime.id)
        form = ReviewForm()
        context = {
            'anime': anime,
            'animes': animes,
            'reviews': Review.objects.filter(anime=anime),
            'form': form,
        }
        if request.user.is_authenticated:
            try:
                context['followed'] = AnimeUserFollowed.objects.get(anime=anime, user=request.user)
            except AnimeUserFollowed.DoesNotExist:
                context['followed'] = None

            try:
                context['ratings'] = UserAnimeRating.objects.filter(anime=anime)
            except UserAnimeRating.DoesNotExist:
                context['ratings'] = None

            try:
                context['rating'] = UserAnimeRating.objects.get(anime=anime, user=request.user)
            except UserAnimeRating.DoesNotExist:
                context['rating'] = None
        return render(request, 'anime-details.html', context)


    elif request.method == 'POST':
        if request.user.is_authenticated:
            anime = get_object_or_404(Anime, slug=slug)
            form = ReviewForm({'user': request.user, 'anime': anime, 'text': request.POST['text']})
            if form.is_valid():
                form.save()
                return redirect("Anima:anime", anime.slug)
        return HttpResponseRedirect(reverse('Anima:anime', kwargs={"slug": slug}))


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


def player_view(request, slug, episode):
    anime = Anime.objects.get(slug=slug)
    ep = anime.player.videos.get(episode=episode)
    videos = anime.player.videos.all()
    return render(request, 'anime-watching.html', {
        "anime": anime,
        "video": ep,
        "videos": videos
    })


def generic_category_view(request, name):
    animes = Anime.objects.all()
    if name == 'Trending':
        animes = Anime.objects.filter(trending=True)
    if name == 'Popular':
        animes = Anime.objects.filter(popular=True)
    if name == 'Recently_Added':
        animes = Anime.objects.all().order_by('-date_added')
    top_views = Anime.objects.all().order_by('-views')[:4]
    paginator = Paginator(animes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'generic_categories.html'
    context = {
        'animes': animes,
        'page_obj': page_obj,
        'top_views': top_views,
        'name': name
    }
    return render(request, template, context)


def category_view(request, slug):
    genre = Genre.objects.get(slug=slug)
    animes = Anime.objects.filter(categories__in=[genre])
    top_views = Anime.objects.all().order_by('-views')[:4]
    paginator = Paginator(animes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'categories.html'
    context = {
        'genre': genre,
        'animes': animes,
        'page_obj': page_obj,
        'reviews': Review.objects.all(),
        'top_views': top_views
    }
    return render(request, template, context)


def user_page_view(request, username):
    if request.user.is_authenticated and request.user.username == username:
        can_edit = True
        return render(request, 'userPage.html', {
            "can_edit": can_edit,
            "current_user": request.user,
            "followed": AnimeUserFollowed.objects.filter(user=request.user),
        })
    if request.user.is_authenticated and request.user.email == username:
        can_edit = True
        return render(request, 'userPage.html', {
            "can_edit": can_edit,
            "current_user": request.user,
            "followed": AnimeUserFollowed.objects.filter(user=request.user),
        })
    User = get_user_model()
    for user in User.objects.all():
        if user.username == username or user.email == username:
            can_edit = False
            return render(request, 'userPage.html', {
                "can_edit": can_edit,
                "current_user": user,
                "followed": AnimeUserFollowed.objects.filter(user=user),
            })
    return HttpResponseRedirect(reverse('Anima:index'))


def user_edit_view(request, username):
    if request.user.is_authenticated and request.user.username == username or request.user.email == username:
        if request.method == 'GET':
            form = UserForm()
            return render(request, 'userEdit.html', {
                "form": form
            })
        if request.method == 'POST':
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                if form.cleaned_data['image']:
                    request.user.image = form.cleaned_data['image']
                if form.cleaned_data['username']:
                    request.user.username = form.cleaned_data['username']
                if form.cleaned_data['birth_date']:
                    request.user.birth_date = form.cleaned_data['birth_date']
                if form.cleaned_data['city']:
                    request.user.city = form.cleaned_data['city']
                if form.cleaned_data['gender']:
                    request.user.gender = form.cleaned_data['gender']
                if form.cleaned_data['about']:
                    request.user.about = form.cleaned_data['about']
                request.user.save()
                return HttpResponseRedirect(reverse('Anima:userpage', kwargs={'username': request.user.username if request.user.username else request.user.email}))

            form = UserForm()
            return render(request, 'userEdit.html', {
                "form": form
            })
    return HttpResponseRedirect(reverse('Anima:index'))



def add_remove_follow(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Anima:anime', kwargs={"slug": slug}))
    anime = Anime.objects.get(slug=slug)
    status = AnimeUserFollowed.objects.filter(user=request.user, anime=anime)
    if status:
        status.delete()
        return HttpResponseRedirect(reverse('Anima:anime', kwargs={"slug": slug}))
    status = AnimeUserFollowed(user=request.user, anime=anime)
    status.save()
    return HttpResponseRedirect(reverse('Anima:anime', kwargs={"slug": slug}))


def set_score(request, slug, rating):
    if rating > 10:
        return HttpResponseRedirect(reverse('Anima:anime', kwargs={"slug": slug}))
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('Anima:anime', kwargs={"slug": slug}))
    anime = Anime.objects.get(slug=slug)
    try:
        score = UserAnimeRating.objects.get(user=request.user, anime=anime)
        score.rating = rating
        score.save()
        return HttpResponseRedirect(reverse('Anima:anime', kwargs={"slug": slug}))
    except UserAnimeRating.DoesNotExist:
        score = UserAnimeRating(user=request.user, anime=anime, rating=rating)
        score.save()
        return HttpResponseRedirect(reverse('Anima:anime', kwargs={"slug": slug}))
