from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout

from core.forms.account import LoginForm
from core.models import ProcessingModel, InputFileModel


class LoginView(View):
    template_name = 'core/login.html'
    form_class = LoginForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('core:dashboard')

        return render(request, self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)

        if not form.is_valid():
            messages.error(request, 'Некорректное имя пользователя или пароль')
            return render(request, self.template_name)

        user = authenticate(request, username=form.cleaned_data["username"], password=form.cleaned_data["password"])

        if user is not None:
            login(request, user)
            messages.success(request, 'Добро пожаловать!')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')

        return render(request, self.template_name)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, 'Вы вышли из системы')
        return redirect('core:login')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'core/profile.html'

    def get(self, request):
        context = {
            'files_count': InputFileModel.objects.filter(user=request.user).count(),
            'runs_count': ProcessingModel.objects.filter(user=request.user).count(),
        }
        return render(request, self.template_name, context=context)
