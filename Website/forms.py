from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from Website.models import *
from phonenumber_field.formfields import PhoneNumberField


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
        if Teacher.objects.filter(user=user).exists():
            self.fields['subject'].queryset = Teacher.objects.get(
                user=user).subjects.all()
        else:
            self.fields['subject'].queryset = Subject.objects.all()

    class Meta:
        model = Lesson
        exclude = ['teacher']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time_start': forms.DateInput(attrs={'type': 'time'}),
            'time_end': forms.DateInput(attrs={'type': 'time'}),
        }


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
    phone = PhoneNumberField(
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
