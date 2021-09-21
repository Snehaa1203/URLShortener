from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import shorturl
import random,string
# Create your views here.

@login_required(login_url='/login/')
def dashboard(request):
    usr = request.user
    urls = shorturl.objects.filter(user=usr) #getting all urls of a particular user(request.user)
    context={'urls': urls}
    return render(request, 'dashboard.html',context)


def randomgen(): #generating random string in lower case ascii of 6 length
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(6))


def generate(request):
    if request.method == "POST":
        # generate url
        pass
        if request.POST['original'] and request.POST['short']:
            # generate based on user input if custom input is given
            user = request.user
            original = request.POST['original']
            short = request.POST['short']
            check = shorturl.objects.filter(short_query=short) #if it exists in db
            if not check:
                newurl = shorturl(
                    user=user,
                    original_url=original,
                    short_query=short,
                )
                newurl.save() #else we create and save it
                return redirect(dashboard)
            else:
                messages.error(request, "Already Exists") #custom input given by user already exists
                return redirect(dashboard)
        elif request.POST['original']:
            # generate randomly  as custom input is not defined
            user = request.user
            original = request.POST['original']
            generated = False
            while not generated:
                short = randomgen()
                check = shorturl.objects.filter(short_query=short)
                if not check:
                    newurl = shorturl(
                        user=user,
                        original_url=original,
                        short_query=short,
                    )
                    newurl.save()
                    return redirect(dashboard)
                else:
                    continue
        else:
            messages.error(request, "Empty Fields")
            return redirect(dashboard)
    else:
        return redirect('dashboard')

def home(request, query=None):
    if not query or query is None:
        return render(request, 'home.html')  
    else:
        try:
            check = shorturl.objects.get(short_query=query)
            check.visits = check.visits + 1  #increase count on each visit
            check.save()
            url_to_redirect = check.original_url #redirecting short url to original link
            return redirect(url_to_redirect)
        except shorturl.DoesNotExist:
            return render(request, 'home.html', {'error': "error"}) #else send error it doesnt exist and link to dashboard




@login_required(login_url='login')
def deleteurl(request):
    if request.method == "DELETE":
        short = request.DELETE
        check = shorturl.objects.filter(short_query=short)
        check.delete()
        return redirect(dashboard)
    
    else:
        return redirect(dashboard)
