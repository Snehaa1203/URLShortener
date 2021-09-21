from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import shortUrl
# Create your views here.

@login_required(login_url='/login/')
def dashboard(request):
    usr = request.user
    urls = shortUrl.objects.filter(user=usr)
    return render(request, 'dashboard.html', {'urls': urls})


