from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.generic import View, CreateView, ListView, DeleteView
from .models import Locker
from .forms import LockerForm
from django.shortcuts import reverse, redirect
from django.http import HttpResponseRedirect, Http404
from rest_framework import viewsets
from .serializers import UserSerializer
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.


class LoginUser(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, "list.html")
        return render(request, "login.html")
    

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


@method_decorator(login_required, name='dispatch')
class CreateLocker(CreateView):
    model = Locker
    template_name = 'locker.html'
    form_class = LockerForm
    success_url = '/list'
    # def dispatch(self, *args, **kwargs):
    #     import ipdb ; ipdb.set_trace()
    #     if not self.request.user.is_authenticated:
    #         return redirect("login_page")
    #     return super().dispatch(*args, **kwargs)

@login_required
def view_locker(request):
    lockers = Locker.objects.all()
    locker_form = LockerForm
    if request.method == 'GET':
        return render(request, 'list.html', {
            'lockers' : lockers,
            'locker_form': locker_form,
        })
    
    if request.method == 'POST':
        if Locker.objects.filter(name = request.POST['name'], key = request.POST['key']).exists():
            return HttpResponse("the name and the key successfully matched")
        return HttpResponse("not matched")
        
class DeleteLocker(DeleteView):
    model = Locker
    success_url = '/list'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login_page")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        return render(request, 'delete.html',{
            'lockers' : Locker.objects.filter(user_id = request.user.pk),
            'locker_form' : LockerForm,
        })   
    
    def get_object(self, queryset = None):
        try:
            obj = Locker.objects.get(name = self.request.POST['name'], key = self.request.POST['key'], user_id = self.request.user.pk)
        except Locker.DoesNotExist:
            raise Http404
        return obj


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

