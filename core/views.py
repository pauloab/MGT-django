from django.http import Http404, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as logout_user  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.forms import NewUserForm, TareaForm
from core.models import Tarea


def home_view(request):
    return render(request, "home.html")

def logout(request):
    logout_user(request)
    return redirect("home")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("list_tasks")
            else:
                messages.error(
                    request, "Nombre de usuario o contraseña no válido.")
        else:
            messages.error(
                request, "Nombre de usuario o contraseña no válido.")
    form = AuthenticationForm()
    return render(request=request, template_name="auth/login.html", context={"login_form": form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro satisfactorio.")
            return redirect("list_tasks")
        messages.error(request, "Verifique la información")
    form = NewUserForm()
    return render(request=request, template_name="auth/register.html", context={"register_form": form})

@login_required(login_url='login') 
def delete_task(request, pk):
    if request.method == 'GET':
        task = Tarea.objects.get(id=pk, user=request.user)
        if task:
            task.delete()
            return redirect('list_tasks')
        return Http404()
    return HttpResponseBadRequest() 

def pay_task(request, pk):
    if request.method == 'GET':
        task = Tarea.objects.get(id=pk, user=request.user)
        if task:
            task.cancelado = True
            task.save()
            return redirect('list_tasks')
        return Http404()
    return HttpResponseBadRequest() 

class createTask(LoginRequiredMixin, CreateView):
    template_name = 'tarea.html'
    form_class = TareaForm
    success_url = '/tasks/list'
    login_url = '/login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class listTasks(LoginRequiredMixin, ListView):
    model = Tarea
    login_url = '/login'
    template_name = 'tareas.html'
    paginate_by = 25  
    ordering = ['-fecha_tarea']
    def get_queryset(self):
        return Tarea.objects.filter(user=self.request.user).all()

class detailTask(LoginRequiredMixin, DetailView):
    model = Tarea
    template_name = 'tarea_view.html'
    login_url = '/login'

    def get_queryset(self):
        return Tarea.objects.filter(user=self.request.user).all()


class updateTask(LoginRequiredMixin, UpdateView):
    model = Tarea
    template_name = 'tarea.html'
    form_class = TareaForm
    success_url = '/tasks/list'
    login_url = '/login'

