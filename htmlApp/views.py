from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# Create your views here.


def home(request):
    return render(request, 'index.html')


@login_required
def homepage(request):
    user = request.user
    return render(request, 'home/homepage.html', {'user': user})
