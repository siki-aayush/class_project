from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.views.generic import CreateView, ListView
from .models import Lockers
from .forms import LockerForm
from django.shortcuts import reverse, redirect
from django.http import HttpResponseRedirect
# Create your views here.



class LoginUser(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponse("user is already logged in")
        return render(request, "login.html")
        # return HttpResponse("hello")
    

    def post(self, request, *args, **kwargs):
        posted_data = request.POST
        username = posted_data["username"]
        password = posted_data["password"]
        
        if username is not None and password is not None:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("successfully logged in")
        
        return HttpResponse("no user found")


def logoutuser(request):
    logout(request)
    return HttpResponse("log out successfully")


class CreateLocker(CreateView):
    template_name= 'locker.html'
    model = Lockers
    form_class = LockerForm
    success_url = '../list'
    def form_valid(self, form):
        obj=form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)

        #return HttpResponseRedirect(self.get_success_url())
        # form.instance.user = self.request.user
        # return super().form_valid(form)


def view_locker(request):
    # import ipdb;ipdb.set_trace()
    lockers = Lockers.objects.all()
    # lockers = Lockers.objects.all().filter(user=request.user)
    locker_form = LockerForm
    if request.method == 'GET':
        # import ipdb;ipdb.set_trace()
        return render(request, 'list.html', {
            'lockers' : lockers,
            'locker_form': locker_form,
        })
    
    if request.method == 'POST':
        # import ipdb;ipdb.set_trace()
        for i in lockers:
            if i.name == request.POST['name'] and i.key == request.POST['key']:
                return HttpResponse("the name and the key successfully matched")
        return HttpResponse("hello")
