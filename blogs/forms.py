from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Blog


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ("title", "description", "tags")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs["placeholder"] = field.label
            field.widget.attrs["class"] = "designer-input"

            if not field.label == "Tags":
                field.label = ""


class CommentForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

    comment = forms.CharField(
        label="Comment", max_length=225,
        widget=forms.TextInput(attrs={'placeholder': 'Comment', "class": "designer-input"})
    )


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""

    username = forms.CharField(
        label="Username", max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Username', "class": "designer-input"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', "class": "designer-input"})
    )


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = User

    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'designer-input'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email','class': 'designer-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'designer-input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password','class': 'designer-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['password2'].label = "Confirm Password"
        for key, field in self.fields.items():
            field.label = ""