# Create your views here.
import random
import string

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, redirect

from .models import ShortUrl


def home(request, query=None):
    if not query:
        return render(request, 'home.html', {})
    else:
        print(f'This was the query {query}')
        try:
            check = ShortUrl.objects.get(short_query=query)
            if check:
                check.visits = F('visits') + 1
                check.save()
                return redirect(check.original_url)
        except ShortUrl.DoesNotExist:
            return render(request, 'home.html', {'error': 'Page does not exist'})


@login_required(login_url='/signin/')
def dashboard(request):
    user = request.user
    url = ShortUrl.objects.filter(user=user)
    return render(request, 'dashboard.html', {'url': url})


def random_gen():
    code = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    return code


@login_required(login_url='/signin/')
def generate(request):
    if request.method == 'POST':
        if request.POST['original'] and request.POST['short']:
            print('Generating based on user input')
            user = request.user
            original = request.POST['original']
            short = request.POST['short']
            check = ShortUrl.objects.filter(short_query=short)
            if not check:
                new_url = ShortUrl(
                    user=user,
                    original_url=original,
                    short_query=short,
                )
                new_url.save()
                return redirect(dashboard)
            else:
                messages.error(request, 'Already exists')
                return redirect(dashboard)
            # ShortUrl.objects.create(
            #     original_url:
            # )
        elif request.POST['original']:
            user = request.user
            original = request.POST['original']
            code = random_gen()
            check = ShortUrl.objects.filter(short_query=code)
            if not check:
                new_url = ShortUrl(
                    user=user,
                    original_url=original,
                    short_query=code,
                )
            new_url.save()
            return redirect(dashboard)
        else:
            messages.error(request, 'Empty fields')
            return redirect(dashboard)
    else:
        return redirect('/dashboard')


def stats(request, query=None):
    if not query:
        return render(request, 'stats.html', {'error': 'Provide a URL'})
    else:
        print(f'This was the query {query}')
        check = ShortUrl.objects.get(short_query=query)
        if check:
            return render(request, 'stats.html', {
                'url': check,
            })
        else:
            return render(request, 'stats.html', {'error': 'Page does not exist'})
    return render(request, 'stats.html', {})
