from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
# Create your views here.
from django.http import HttpResponse
import openai
openai.api_key = ''


# Create your views here.

def index(request):
    return render(request, 'app/index.html')


def pricing(request):
    return render(request, 'app/pricing.html')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'app/login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('app'))
        else:
            return render(request, 'app/login.html', {
                'message': 'Invalid Credentials'
            })

def app(request):
    if request.user.is_authenticated:
        return render(request, 'app/app.html')
    else:#DONE
        return render(request, 'app/message.html')

def app_next(request):
    if request.method == 'POST':
        return render(request, 'app/app_2.html', {
            'points': range(int(request.POST['main-points'])),
            'title': request.POST['title']
        })
    else:
        return render(request, 'app/message.html', {
            'message': 'Wrong path. If you are trying to generate an article, you can click on "App".'
        })

def finish(request):
    if request.method == 'POST':
        iterator = range(len(request.POST) - 2)
        title = request.POST['title']
        main_points = []
        paragraphs = []
        for x in iterator:
            if request.user.credits > 0:
                main_point = request.POST[str(x + 1)]
                main_points.append(main_point)
                paragraph = openai.Completion.create(
                                engine='text-davinci-003',
                                prompt=title + '\n\n Continue the following point\n' + main_point + ":",
                                max_tokens=256,
                                temperature=0.7
                            )
                tokens_used = paragraph['usage']['total_tokens']
                if request.user.credits - tokens_used < 1:
                    request.user.credits = 0
                    request.user.save()
                else:
                    request.user.credits -= tokens_used
                    request.user.save()
                paragraph = paragraph['choices'][0]['text']
                paragraph = paragraph.lstrip() + '<br /><br />'
                paragraphs.append(paragraph)
            else:
                main_point = request.POST[str(x + 1)]
                main_points.append(main_point)
                paragraphs.append('Not Enough Tokens.')
        return render(request, 'app/finish.html', {
            'content': zip(main_points, paragraphs),
            'title': title,
        })

def logout_view(request):
    try:
        logout(request)
        return HttpResponseRedirect(reverse('index'))
    except:
        return render(request, 'app/message.html')

def usage(request):
    return render(request, 'app/usage.html')
