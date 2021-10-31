import datetime
import secrets
import string
from operator import attrgetter

import pytz
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
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
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

    def __init__(self):
        super().__init__()
        self.template_name = 'index.html'
        self.context = dict()
        self.messages = []

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
            'messages': self.messages,
        })

    def base_render(self, request):
        """Function to render page with context."""
        return render(request, self.template_name, self.context)

    @staticmethod
    def get_base_menu(request) -> list:
        """Function to obtain the basic parameters of the context."""
        menu = [
            {"label": "Головна", "url": "/"},
        ]
        if request.user.is_authenticated:
            s_class = Student.objects.get(
                user=request.user).s_class if Student.objects.filter(
                user=request.user).exists() else None
            if s_class is None:
                dropdown = []
                for s_class in Class.objects.all():
                    dropdown.append(
                        {"label": s_class, "url": f"/schedule/?class={s_class}"}
                    )
                menu.append(
                    {
                        "label": "Розклад", "dropdown": dropdown
                    }
                )
            else:
                menu.append({"label": "Розклад", "url": "/schedule/"})
            if Teacher.objects.filter(user=request.user).exists():
                menu.append({"label": "Створити урок", "url": "/create/"})
        else:
            menu.append({"label": "Розклад", "url": "/schedule/"})

        for it in range(len(menu)):
            if not "dropdown" in menu[it]:
                if menu[it]["url"] == request.path:
                    menu[it]["active"] = 'active'
            else:
                for dropdown_it in range(len(menu[it]["dropdown"])):
                    if menu[it]["dropdown"][dropdown_it][
                        "url"] == str(request.path) + '?class=' + str(
                        get_class(request)):
                        menu[it]["dropdown"][dropdown_it]["active"] = 'active'
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
        self.user = None
        self.template_name = 'registration/login.html'

    def post(self, request):
        """Redefining "post" function to login user."""
        super().post(request)
        self.check_user_existence(request)
        if self.user is not None and self.user.is_active:
            login(request, self.user)
            return redirect('home')
        self.context.update({
            'login_form': LoginForm(request.POST),
        })
        self.messages.append('Неправильний логін/email чи пароль')
        return self.base_render(request)

    def get(self, request):
        """Redefining "get" function to create login form."""
        super().get(request)
        if request.user.is_authenticated:
            return redirect('home')
        self.context['login_form'] = LoginForm()
        return self.base_render(request)

    def check_user_existence(self, request):
        self.user = None
        if User.objects.filter(email=request.POST.get('username')).exists():
            user = User.objects.get(email=request.POST.get('username'))
            self.user = authenticate(username=user.username,
                                     password=request.POST.get('password')
                                     )
        if User.objects.filter(username=request.POST.get('username')).exists():
            self.user = authenticate(username=request.POST.get('username'),
                                     password=request.POST.get('password')
                                     )


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
            if not User.objects.filter(email=form.data[
                'email']).exists() and not User.objects.filter(
                username=form.data['username']).exists():
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
                    'Користувач з таким самим логіном чи email вже існує')
        else:
            self.messages.append('Помилка в заповненні форми')
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
        """To logout a user."""
        logout(request)
        return redirect('home')


class ProfileView(LoginRequiredMixin, BaseView):
    """
    View of the profile page. Supports both teacher and student account type.
    """
    login_url = '/login/'

    def __init__(self):
        super().__init__()
        self.template_name = 'profile.html'

    def get(self, request):
        super().get(request)
        self.set_profile_change_form(request)
        self.get_user_info(request)
        self.get_invitation_codes(request)
        self.context.update({"codes_form": CreateInvitationForm()})
        return self.base_render(request)

    def set_profile_change_form(self, request):
        form = ChangeProfileForm()
        form.fields['username'].initial = request.user.username
        form.fields['email'].initial = request.user.email
        form.fields['first_name'].initial = request.user.first_name
        form.fields['last_name'].initial = request.user.last_name
        if Teacher.objects.filter(user=request.user).exists():
            form.fields['subjects'].initial = Teacher.objects.get(
                user=request.user).subjects.all()
            form.fields['phone'].initial = Teacher.objects.get(
                user=request.user).phone
            form.fields['show_phone'].initial = Teacher.objects.get(
                user=request.user).show_phone
        else:
            del form.fields['subjects']
            del form.fields['phone']
            del form.fields['show_phone']
        if Student.objects.filter(user=request.user).exists():
            s_class = Student.objects.get(user=request.user).s_class
            form.fields['s_class'].initial = s_class
        else:
            del form.fields['s_class']
        self.context.update({"profile_change_form": form})

    def save_profile_change_form(self, request):
        form = ChangeProfileForm(request.POST)
        if "change_profile" in request.POST:
            if not Teacher.objects.filter(user=request.user).exists():
                del form.fields['subjects']
            if not Student.objects.filter(user=request.user).exists():
                del form.fields['s_class']
            self.context.update({"profile_change_form": form})
            if form.is_valid():
                if form.cleaned_data["username"] != request.user.username:
                    request.user.username = form.cleaned_data["username"]
                if form.cleaned_data["first_name"] != request.user.first_name:
                    request.user.first_name = form.cleaned_data["first_name"]
                if form.cleaned_data["last_name"] != request.user.last_name:
                    request.user.last_name = form.cleaned_data["last_name"]
                if form.cleaned_data["email"] != request.user.email:
                    request.user.email = form.cleaned_data["email"]
                if Teacher.objects.filter(user=request.user).exists():
                    teacher = Teacher.objects.get(user=request.user)
                    if form.cleaned_data["subjects"] != teacher.subjects.all():
                        teacher.subjects.set(form.cleaned_data["subjects"])
                    if form.cleaned_data["phone"] != teacher.phone:
                        teacher.phone = form.cleaned_data["phone"]
                    if form.cleaned_data["show_phone"] != teacher.show_phone:
                        teacher.show_phone = form.cleaned_data["show_phone"]
                    teacher.save()
                if Student.objects.filter(user=request.user).exists():
                    student = Student.objects.get(user=request.user)
                    if form.cleaned_data["s_class"] != student.s_class and \
                            form.cleaned_data["s_class"]:
                        student.s_class = form.cleaned_data["s_class"]
                    student.save()
                request.user.save()
            else:
                self.messages.append("Форма заповнена неправильно")
        else:
            self.set_profile_change_form(request)

    def get_user_info(self, request):
        self.context.update({"user": request.user})
        user_type = []
        if Student.objects.filter(user=request.user).exists():
            user_type.append("student")
            student = Student.objects.get(user=request.user)
            if student.s_class is None:
                self.context.update({"noclass": True})
            self.context.update(
                {"student": student})
        if Teacher.objects.filter(user=request.user).exists():
            user_type.append("teacher")
            self.context.update(
                {"teacher": Teacher.objects.get(user=request.user)})
        if request.user.is_superuser:
            user_type.append("admin")
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
        self.save_profile_change_form(request)
        self.process_code_creation(request)
        self.process_code_deletion(request)
        self.get_user_info(request)
        self.get_invitation_codes(request)
        return self.base_render(request)

    def process_code_creation(self, request):
        form = CreateInvitationForm(request.POST)
        if 'create_codes' in request.POST:
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
            self.context.update({"codes_form": form})

    @staticmethod
    def process_code_deletion(request):
        if "delete_code" in request.POST:
            Invitation.objects.filter(invitor=request.user,
                                      code=request.POST["del_code"]).delete()


def get_class(request):
    s_class = None
    if Student.objects.filter(user=request.user).exists():
        s_class = Student.objects.get(user=request.user).s_class
    if s_class is None:
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
    return s_class


class ScheduleView(LoginRequiredMixin, BaseView):
    """A view for schedule page."""
    login_url = '/login/'

    def __init__(self):
        super().__init__()
        self.lessons = []
        self.week = None
        self.weekday = tuple
        self.date = None
        self.template_name = 'schedule.html'

    def get(self, request):
        super().get(request)
        self.get_date(request)
        self.get_date_buttons_urls(request)
        s_class = get_class(request)
        self.context.update({"class": s_class})
        self.lessons = Lesson.objects.filter(s_class=s_class)
        self.sort_lessons(request)
        self.create_table(request)
        self.ask_for_class(request)
        return self.base_render(request)

    def ask_for_class(self, request):
        if Student.objects.filter(user=request.user).exists():
            s_class = Student.objects.get(user=request.user).s_class
            if s_class is None:
                self.messages.append(
                    "Увага! Клас не обран! "
                    "Перейдіть до профіля і оберіть клас."
                )

    def get_date_buttons_urls(self, request):
        date = self.date
        self.weekday = date.weekday()
        date += timezone.timedelta(days=-self.weekday)
        next_week_day = dateformat.format(
            date + timezone.timedelta(days=7),
            'Y-m-d'
        )
        last_week_day = dateformat.format(
            date + timezone.timedelta(days=-7),
            'Y-m-d'
        )
        date_from = datetime.datetime.combine(date,
                                              datetime.time(0, 0)).replace(
            tzinfo=pytz.timezone("Europe/Kiev"))
        date_to = datetime.datetime.combine(
            date_from + timezone.timedelta(days=6),
            datetime.time(23, 59)).replace(
            tzinfo=pytz.timezone("Europe/Kiev"))
        self.week = (date_from, date_to)
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

    def sort_lessons(self, request):
        lessons = []
        for lesson in self.lessons:
            if self.week[0] <= datetime.datetime.combine(
                    lesson.date, datetime.time(0, 0)
            ).replace(tzinfo=pytz.timezone("Europe/Kiev")) <= self.week[1]:
                lessons.append(lesson)
        lessons.sort(key=attrgetter("time_start"))
        self.lessons = lessons

    def create_table(self, request):
        table = []
        for day in range(7):
            date_from = self.week[0] + timezone.timedelta(days=day)
            date_to = self.week[0] + timezone.timedelta(days=day + 1)
            day_lessons = []
            for lesson in self.lessons:
                if date_from <= datetime.datetime.combine(lesson.date,
                                                          lesson.time_start).replace(
                    tzinfo=pytz.timezone("Europe/Kiev")) < date_to:
                    day_lessons.append(lesson)
            table.append(day_lessons)
        self.context.update({"table": table})


class LessonCreateView(LoginRequiredMixin, BaseView):
    """A view for page where a teacher can create a lesson."""
    login_url = '/login/'

    def __init__(self):
        super().__init__()
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
            if "http://" in lesson.link:
                lesson.link = lesson.link[7:]
            elif "https://" in lesson.link:
                lesson.link = lesson.link[8:]
            lesson.teacher = Teacher.objects.get(user=request.user)
            lesson.save()
            self.messages.append(
                f"Урок {lesson.subject} на {lesson.time_start.strftime('%H:%M:%S')} успішно створений")
            self.context.update({"form": form})
        else:
            self.messages.append("Форма заповнена неправильно")
        return self.base_render(request)
