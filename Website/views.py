import secrets
import string

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils import dateformat
from django.views import View

from Website.forms import *
from Website.models import Invitation, Student, Teacher


class BaseView(View):
    """
    Base view class; every page view class is a child of BaseView;
    has get and post functions,
    that are called when get or post methods are used;
    has a template_name in init that must be redefined in child class;
    """

    def __init__(self):
        super().__init__()
        self.template_name = 'index.html'
        self.context = dict()
        self.messages = []
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
            'messages': self.messages,
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
        ]

        if Teacher.objects.filter(user=request.user).exists():
            dropdown = []
            for s_class in Class.objects.all():
                dropdown.append(
                    {"label": s_class, "url": f"/schedule?class={s_class}"}
                )
            menu.append(
                {
                    "label": "Розклад", "dropdown": dropdown
                }
            )
            menu.append({"label": "Створити урок", "url": "/create/"})
        else:
            menu.append({"label": "Розклад", "url": "/schedule/"})

        for it in range(len(menu)):
            if not "dropdown" in menu[it]:
                if menu[it]["url"] == request.path:
                    menu[it]["active"] = 'active'
            else:
                for dropdown_it in range(len(menu[it]["dropdown"])):
                    if menu[it]["dropdown"][dropdown_it]["url"] == request.path:
                        menu[it]["active"] = 'active'
        return menu


class IndexView(BaseView):
    """View of main website page"""

    def __init__(self):
        super().__init__()
        self.template_name = 'index.html'

    def get(self, request):
        super().get(request)
        teachers = Teacher.objects.all()
        self.context.update({"teachers": teachers})
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
        })
        self.messages.append('Неверный логин или пароль')
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
                    self.messages.append(
                        'Введено невірний код, або цей код вже використано')
            else:
                self.messages.append(
                    'Пользователь с таким же email уже существует')
        else:
            self.messages.append('Ошибка в заполнении формы')
        self.context.update({
            'registration_form': form,
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
    """
    View of the profile page. Supports both teacher and student account type.
    """

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
                self.context.update({"codes_form": form})
                self.messages.append("Форма заповнена неправильно")
        else:
            form = CreateInvitationForm()
            self.context.update({"codes_form": form
                                 })

    @staticmethod
    def process_code_deletion(request):
        if request.POST.get("del_code", None):
            Invitation.objects.filter(invitor=request.user,
                                      code=request.POST["del_code"]).delete()


class ScheduleView(BaseView):
    """A view for schedule page."""

    def __init__(self):
        super().__init__()
        self.date = None
        self.login_required = True
        self.template_name = 'schedule.html'

    def get(self, request):
        super().get(request)
        self.get_date(request)
        self.get_date_buttons_urls(request)
        s_class = self.get_class(request)
        lessons = Lesson.objects.filter(s_class=s_class)
        weekday = self.date.weekday()
        table = [lessons.filter()]
        return self.base_render(request)

    def get_class(self, request):
        if Student.objects.filter(user=request.user).exists():
            s_class = Student.objects.get(user=request.user).s_class
        else:
            s_class_str = request.GET.get('class', None)
            if s_class_str is None:
                s_class = Class.objects.all()[0]
            else:
                digit = s_class_str.split('-')[0]
                letter = s_class_str.split('-')[1]
                if Class.objects.filter(digit=digit, letter=letter).exists():
                    s_class = Class.objects.get(digit=digit, letter=letter)
                else:
                    s_class = Class.objects.all()[0]
        self.context.update({"class": s_class})
        return s_class

    def get_date_buttons_urls(self, request):
        date = self.date
        weekday = date.weekday()
        date += timezone.timedelta(days=-weekday)
        next_week_day = dateformat.format(
            date + timezone.timedelta(days=7),
            'Y-m-d'
        )
        last_week_day = dateformat.format(
            date + timezone.timedelta(days=-7),
            'Y-m-d'
        )
        date = dateformat.format(date, 'M. d') + ' - ' + dateformat.format(
            date + timezone.timedelta(days=6), 'M. d, Y')
        self.context.update({"date": date})
        self.context.update({"last_week_day": last_week_day})
        self.context.update({"next_week_day": next_week_day})

    def get_date(self, request):
        date_str = request.GET.get('date', None)
        if date_str is None:
            date = timezone.now()
        else:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        self.date = date


class LessonCreateView(BaseView):
    """A view for page where a teacher can create a lesson."""

    def __init__(self):
        super().__init__()
        self.login_required = True
        self.template_name = 'create_lesson.html'

    def get(self, request):
        super().get(request)
        form = CreateLessonForm(request.user)
        self.context.update({"form": form})
        return self.base_render(request)

    def post(self, request):
        super().post(request)
        form = CreateLessonForm(request.user, request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.teacher = Teacher.objects.get(user=request.user)
            lesson.save()
            self.messages.append(
                f"Урок {lesson.subject} на {lesson.time_start.strftime('%H:%M:%S')} успішно створений")
            self.context.update({"form": form})
        else:
            self.messages.append("Форма заповнена неправильно")
        return self.base_render(request)
