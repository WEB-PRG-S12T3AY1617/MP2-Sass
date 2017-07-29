from django import forms
from . models import User

class RegisterForm(forms.ModelForm):
    help = {
        'name': 'Required',
        'email': 'Required, must also be a valid email address',
        'password': 'Required, must be at least 8 characters long'
    }

    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'type','contact_num', 'picture']

        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'password': 'Password',
            'contact_num': 'Contact Number',
            'picture': 'Profile Picture',
            'type': 'Account Type',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john.doe@gmail.com'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'contact_num': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+63 123 456 7890'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'type': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['contact_num'].required = False
        self.fields['picture'].required = False


class LogInForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john.doe@gmail.com'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }