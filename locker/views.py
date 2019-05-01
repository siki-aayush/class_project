from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.views.generic import View, CreateView, ListView, DeleteView
from .models import Locker
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
    model = Locker
    template_name = 'locker.html'
    form_class = LockerForm
    success_url = '../list'
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("login_page")
        return super().dispatch(*args, **kwargs)
    
    def form_valid(self, form):
        obj=form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return HttpResponseRedirect(self.success_url)


def view_locker(request):
    lockers = Locker.objects.all()
    locker_form = LockerForm
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect("login_page")
        return render(request, 'list.html', {
            'lockers' : lockers,
            'locker_form': locker_form,
        })
    
    if request.method == 'POST':
        if Locker.objects.filter(name = request.POST['name'], key = request.POST['key']).exists():
            return HttpResponse("the name and the key successfully matched")
        return HttpResponse("not matched")


# # class DeleteLocker(View):
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return redirect("login_page")
#         return super().dispatch(*args, **kwargs)

#     def get(self, request):
#          return render(request, 'delete.html',{
#              'lockers' : Locker.objects.filter(user_id = request.user.pk),
#              'locker_form' : LockerForm,
#          })
# 
#     def post(self, request):
#         if Locker.objects.filter(name = request.POST['name'], key = request.POST['key'], user_id = request.user.pk).exists():
#              Locker.objects.filter(name = request.POST['name'], key = request.POST['key']).delete()
#              return HttpResponse("successfully deleted")
#         return HttpResponse("no locker found")

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
    
    def delete(self, request, *args, **kwargs):
        if Locker.objects.filter(name = request.POST['name'], key = request.POST['key'], user_id = request.user.pk).exists():
            self.object = Locker.objects.get(name = request.POST['name'], key = request.POST['key'], user_id = request.user.pk)
            # return super.delete(request, *args, **kwargs)
            success_url = self.get_success_url()
            self.object.delete()
            return HttpResponseRedirect(success_url)
        return HttpResponse("no lockers found")