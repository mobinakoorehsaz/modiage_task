from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from .serializers import UserSerializer
from rest_framework import generics
from .forms import *


class IndexView(TemplateView):
    """
    main page
    """
    template_name = "main.html"


class Perms(ListView):
    """
    permissions page
    """
    model = User
    template_name = 'permissions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['form'] = CheckboxForm()

        return context


def change_perms(request):
    """
    update user permission by change boolean fields in user model
    """
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CheckboxForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.get(email=data['user'])
            print(user.id)
            print(data)
            if user:
                try:
                    if data['chart_1']:
                        user.chart_1 = True
                        user.save()
                    else:
                        user.chart_1 = False
                        user.save()

                    if data['chart_2']:
                        user.chart_2 = True
                        user.save()
                    else:
                        user.chart_2 = False
                        user.save()
                except ValueError:
                    pass

        return redirect(url)


class UserRegister(CreateView):
    """
    signup page
    """
    model = User
    template_name = 'signup.html'
    form_class = UserCreateForm
    success_url = reverse_lazy('account:user_address')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        login(self.request, user)
        return redirect('account:main_url')


def user_login(request):
    """
    login page
    """
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['email'], password=data['password'])
            print(data)
            if user is not None:
                login(request, user)
                return redirect("account:main_url")
            else:
                return render(request, 'login.html', {'form': form})

    else:
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect("account:main_url")


# APIs

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
