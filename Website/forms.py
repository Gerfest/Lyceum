from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    """Registration form"""
    invitation_code = forms.CharField(
        min_length=5,
        max_length=99,
        label='Код запрошення',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
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
    password1 = forms.CharField(
        min_length=8,
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        min_length=8,
        label='Повторіть пароль',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)


class LoginForm(forms.Form):
    """Login form"""
    username = forms.CharField(
        max_length=150,
        label='Ім\'я користувача',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'placeholder': 'Username',
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
                'placeholder': 'Password',
            }
        ),
    )


class CreateInvitationForm(forms.Form):
    amount = forms.IntegerField(min_value=1, max_value=99,
                                label="Кількість", initial=1)
    type = forms.ChoiceField(widget=forms.Select(),
                             required=True,
                             label="Тип",
                             choices=(("Student", ("Учень")),
                                      ("Teacher", ("Вчитель")))
                             )
