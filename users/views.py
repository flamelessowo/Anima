from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, SignUpForm
from django.contrib.auth import authenticate, login
from django.urls import reverse


def login_view(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            form = LoginForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user = authenticate(email=data['email'], password=data['password'])
                if user:
                    if user.is_active:
                        login(request, user)
                        return HttpResponseRedirect(reverse('Anima:index'))
                    else:
                        return HttpResponse('Disabled account')
                else:
                    return HttpResponse('Invalid login')

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('Anima:index'))
        print(form.errors)

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
