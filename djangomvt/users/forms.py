from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Логін", 
        widget= forms.TextInput(attrs={'class': 'form-control'})
        )
    email = forms.EmailField(
        label="Електронна пошта",
        required=True,
        widget= forms.TextInput(attrs={'class': 'form-control'})
        )
    first_name = forms.CharField(
        label="Ім'я",
        required=True,
        widget= forms.TextInput(attrs={'class': 'form-control'})
        )
    last_name = forms.CharField(
        label="Прізвище",
        required=True,
        widget= forms.TextInput(attrs={'class': 'form-control'})
        )
    image = forms.ImageField(
        label="Зображення",
        required=True,
        widget= forms.FileInput(attrs={'class': 'form-control'})
        )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )
    password2 = forms.CharField(
        label="Повторіть пароль", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'image', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Ця електронна пошта вже зареєстрована")
        return email
    
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email", 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if email and password:
            try:
                user_obj = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Некоректний email або пароль")

            user = authenticate(username=user_obj.username, password=password)
            if user is None:
                raise forms.ValidationError("Некоректний email або пароль")

            self._user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, '_user', None)