from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
import secrets
import string

from Website.forms import SignUpForm, LoginForm, CreateInvitationForm
from Website.models import Invitation, Student, Teacher


class BaseView(View):
    def __init__(self):
        super().__init__()
        self.template_name = 'index.html'
        self.context = dict()
        self.login_required = False

    def get(self, request):
        self.both(request)
        return self.base_context(request)

    def post(self, request):
        self.both(request)
        return self.base_context(request)

    def both(self, request):
        if self.login_required:
            if not request.user.is_authenticated:
                return redirect('login')

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

    def check_login(self):
        self.login_required = True

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
                invitation = Invitation.objects.filter(
                    code=form.data['invitation_code'],
                    activated=False).first()
                if invitation:
                    form.save()
                    if invitation.type == "Student":
                        Student.objects.create(
                            user=User.objects.get(email=form.data['email']))
                    elif invitation.type == "Teacher":
                        Teacher.objects.create(
                            user=User.objects.get(email=form.data['email']))
                    login(request,
                          authenticate(
                              username=form.cleaned_data.get('username'),
                              password=form.cleaned_data.get('password1')))
                    invitation.activated = True
                    invitation.user = User.objects.get(email=form.data['email'])
                    invitation.save()
                    return redirect('home')
                else:
                    message = [
                        'Введено невірний код, або цей код вже використано']
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
        self.check_login()
        self.get_user_info(request)
        self.get_invitation_codes(request)
        self.context.update({"codes_form": CreateInvitationForm()})
        return self.base_render(request)

    def get_user_info(self, request):
        self.context.update({"user": request.user})
        user_type = []
        if Student.objects.filter(user=request.user).exists():
            user_type.append("student")
            self.context.update(
                {"student": Student.objects.get(user=request.user)})
        if Teacher.objects.filter(user=request.user).exists():
            user_type.append("teacher")
            self.context.update(
                {"teacher": Teacher.objects.get(user=request.user)})
        self.context.update({"user_type": user_type})

    def get_invitation_codes(self, request):
        all_codes = Invitation.objects.filter(invitor=request.user)
        codes_non_activated = all_codes.filter(activated=False)
        codes_activated = all_codes.filter(activated=True)
        codes = []
        for i in range(max(len(codes_activated), len(codes_non_activated))):
            codes.append(
                [i,
                 codes_non_activated[i] if i < len(codes_non_activated) else "",
                 codes_activated[i] if i < len(codes_activated) else ""])
        self.context.update({"codes": codes})

    def post(self, request):
        super().post(request)
        self.check_login()
        self.process_code_creation(request)
        self.process_code_deletion(request)
        self.get_user_info(request)
        self.get_invitation_codes(request)
        return self.base_render(request)

    def process_code_creation(self, request):
        form = CreateInvitationForm(request.POST)
        if request.POST.get("del_code", None) is None:
            if form.is_valid():
                self.context.update({"codes_form": CreateInvitationForm()})
                alphabet = string.ascii_letters + string.digits
                for i in range(int(form.data["amount"])):
                    code = ''.join(secrets.choice(alphabet) for _ in range(10))
                    Invitation.objects.create(invitor=request.user,
                                              type=form.data["type"],
                                              code=code)
            else:
                self.context.update({"codes_form": form,
                                     'messages': [
                                         "Форма заповнена неправильно"],
                                     })
        else:
            form = CreateInvitationForm()
            self.context.update({"codes_form": form
                                 })

    def process_code_deletion(self, request):
        if request.POST.get("del_code", None):
            Invitation.objects.filter(invitor=request.user,
                                      code=request.POST["del_code"]).delete()


class ScheduleView(BaseView):
    def __init__(self):
        super().__init__()
        self.template_name = 'schedule.html'

    def get(self, request):
        super().get(request)
        return self.base_render(request)
