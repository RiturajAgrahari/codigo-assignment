from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CommentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

    comment = forms.CharField(
        label="Comment", max_length=225,
        widget=forms.TextInput(attrs={'placeholder': 'Comment', "class": "comment-input"})
    )


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

    username = forms.CharField(
        label="Username", max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Username', "class": "form-input"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', "class": "form-input"})
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = User

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'form-input'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'form-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'form-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['password2'].label = "Confirm Password"
        for key, field in self.fields.items():
            field.label = ""