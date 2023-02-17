import django.forms as forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__exact=email):
            self.add_error('email', 'Email already used')
            return False
        return email