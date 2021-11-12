import pytz
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from phonenumber_field import formfields

from Website.models import *


class SignUpForm(UserCreationForm):
    """Registration form"""
    invitation_code = forms.CharField(
        min_length=5,
        max_length=99,
        label='Код запрошення',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Одноразовий код запрошення видається вчителем',
            }
        )
    )
    username = forms.CharField(
        min_length=5,
        max_length=99,
        label='Ім\'я користувача',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Зазвичай від 5 символів англійською мовою',
            }
        )
    )
    first_name = forms.CharField(
        min_length=1,
        max_length=99,
        label='Ім\'я',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ваше ім\'я',
            }
        )
    )
    last_name = forms.CharField(
        min_length=1,
        max_length=99,
        label='Прізвище',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ваше прізвище',
            }
        )
    )
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ваша електронна пошта',
            }
        )
    )
    password1 = forms.CharField(
        min_length=8,
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Пароль для сайту',
            }
        )
    )
    password2 = forms.CharField(
        min_length=8,
        label='Повторіть пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Повторіть пароль вище',
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2',)


class LoginForm(forms.Form):
    """Login form"""
    username = forms.CharField(
        max_length=150,
        label='Ім\'я користувача чи email',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Ім\'я користувача чи email',
            },
        ),
    )
    password = forms.CharField(
        max_length=150,
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'class': 'form-control',
                'placeholder': 'Пароль',
            }
        ),
    )


class CreateInvitationForm(forms.Form):
    """
    Form that allows to create a certain amount of
    invitations with one of two types
    """
    amount = forms.IntegerField(min_value=1, max_value=99,
                                label="Кількість", initial=1)
    type = forms.ChoiceField(widget=forms.Select(),
                             required=True,
                             label="Тип",
                             choices=(("Student", "Учень"),
                                      ("Teacher", "Вчитель"))
                             )


class CreateLessonForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(CreateLessonForm, self).__init__(*args, **kwargs)
        self.set_widget()
        self.user = user
        self.set_subjects()
        self.set_classes()
        self.set_initials()

    def set_initials(self):
        tz = pytz.timezone("Europe/Kiev")
        now = timezone.now().astimezone(tz)
        time_start = now.replace(minute=0)+timezone.timedelta(hours=1)
        time_end = time_start.replace(minute=45)
        self.initial['time_start'] = time_start.strftime('%H:%M')
        self.initial['time_end'] = time_end.strftime('%H:%M')
        self.initial["date"] = time_start.strftime('%Y-%m-%d')

    def set_classes(self):
        form_control = ['subject', 'date', 'time_start', 'time_end', 's_class',
                        'link', 'type', 'description']
        form_check = ['hide_link']
        for form in form_control:
            self.fields[form].widget.attrs["class"] = 'form-control'
        for form in form_check:
            self.fields[form].widget.attrs["class"] = 'form-check-input'

    def set_subjects(self):
        if Teacher.objects.filter(user=self.user).exists():
            self.fields['subject'].queryset = Teacher.objects.get(
                user=self.user).subjects.all()
        else:
            self.fields['subject'].queryset = Subject.objects.all()

    def set_widget(self):
        self.fields['date'].widget = forms.DateInput(
            attrs={'type': 'date', "value": "2021.11.03"}
        )
        self.fields['time_start'].widget = forms.DateInput(
            attrs={'type': 'time'}
        )
        self.fields['time_end'].widget = forms.DateInput(
            attrs={'type': 'time'}
        )

    class Meta:
        model = Lesson
        exclude = ['teacher']


class ChangeProfileForm(forms.Form):
    """A form that allows to change user info"""
    username = forms.CharField(
        min_length=5,
        max_length=99,
        label='Ім\'я користувача',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        label='Email',
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )
    first_name = forms.CharField(
        min_length=1,
        max_length=99,
        label='Ім\'я',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    last_name = forms.CharField(
        min_length=1,
        max_length=99,
        label='Прізвище',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        label='Предмети',
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={

            }
        )
    )
    phone = formfields.PhoneNumberField(
        label='Телефон',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
    )
    show_phone = forms.BooleanField(
        label="Показувати телефон іншим?",
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
                'role': "switch"
            }
        )
    )
    s_class = forms.ModelChoiceField(
        queryset=Class.objects.all(),
        label='Клас',
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )
