from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View

from Website.forms import SignUpForm, LoginForm


class BaseView(View):
    def __init__(self):
        super().__init__()
        self.template_name = 'index.html'
        self.context = dict()

    def get(self, request):
        return self.base_context(request)

    def post(self, request):
        return self.base_context(request)

    def base_context(self, request):
        """
        Function to obtain the basic parameters of the context and render it
        """
        self.context.update({
            'menu': self.get_base_menu(request),
            'user': request.user,
        })

    def base_render(self, request):
        """Function to render page with context."""
        return render(request, self.template_name, self.context)

    @staticmethod
    def get_base_menu(request) -> list:
        """Function to obtain the basic parameters of the context."""
        menu = [
            {"label": "Головна", "url": "/"},
            {"label": "Розклад", "url": "/schedule/"},
            {"label": "Електронний щоденник", "url": "/diary/"},
        ]
        for it in range(len(menu)):
            if menu[it]["url"] == request.path:
                menu[it]["active"] = 'active'
        return menu


class IndexView(BaseView):
    def __init__(self):
        super().__init__()
        self.template_name = 'index.html'

    def get(self, request):
        super().get(request)
        return self.base_render(request)


class LoginView(BaseView):
    """View Based Class to display login page."""

    def __init__(self):
        """__init__ redefinition."""
        super().__init__()
        self.template_name = 'registration/login.html'

    def post(self, request):
        """Redefining "post" function to login user."""
        super().post(request)
        user = authenticate(username=request.POST.get('username'),
                            password=request.POST.get('password'))
        if user is not None and user.is_active:
            login(request, user)
            return redirect('home')
        self.context.update({
            'login_form': LoginForm(request.POST),
            'messages': ['Неверный логин или пароль'],
        })
        return self.base_render(request)

    def get(self, request):
        """Redefining "get" function to create login form."""
        super().get(request)
        if request.user.is_authenticated:
            return redirect('home')
        self.context['login_form'] = LoginForm()
        return self.base_render(request)


class SignupView(BaseView):
    """View Based Class to display registration page."""

    def __init__(self):
        """__init__ redefinition."""
        super().__init__()
        self.template_name = 'registration/registration.html'

    def post(self, request):
        """Redefining "post" function to initialize user registration."""
        super().post(request)
        form = SignUpForm(request.POST)
        if form.is_valid():
            if not User.objects.filter(email=form.data['email']).exists():
                form.save()
                login(request,
                      authenticate(username=form.cleaned_data.get('username'),
                                   password=form.cleaned_data.get('password1')))
                return redirect('home')
            else:
                message = ['Пользователь с таким же email уже существует']
        else:
            message = ['Ошибка в заполнении формы']
        self.context.update({
            'registration_form': form,
            'messages': message,
        })
        return self.base_render(request)

    def get(self, request):
        """Redefining "get" function to create signup form."""
        super().get(request)
        if request.user.is_authenticated:
            return redirect('home')
        self.context['registration_form'] = SignUpForm()
        return self.base_render(request)


class LogoutView(BaseView):
    """View Based Class for logout."""

    def get(self, request):
        """To logout user."""
        logout(request)
        return redirect('home')


class ProfileView(BaseView):
    def __init__(self):
        super().__init__()
        self.template_name = 'profile.html'

    def get(self, request):
        super().get(request)
        return self.base_render(request)
