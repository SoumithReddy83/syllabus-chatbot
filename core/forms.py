from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import Syllabus
from django.contrib.auth.forms import PasswordResetForm



# Signup Form
class UserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']


# Login Form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput)

class SyllabusUploadForm(forms.ModelForm):
    class Meta:
        model = Syllabus
        fields = ['department', 'course_number', 'course_name', 'syllabus_file']

    def clean_syllabus_file(self):
        file = self.cleaned_data.get('syllabus_file')
        if not file.name.endswith('.pdf'):
            raise forms.ValidationError('Only PDF files are allowed.')
        return file
    
class AskQuestionForm(forms.Form):
    syllabus_id = forms.IntegerField(widget=forms.HiddenInput)
    question = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label="Your Question")


class ForgotUsernameForm(forms.Form):
    email = forms.EmailField(label='Registered Email')