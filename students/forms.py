from django.contrib.auth.models import User
from django import forms
from courses.models import Course


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'id': 'floatingPassword1'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': "Confirm Password", 'class': "form-control", 'id': 'floatingPassword2'}))
    class Meta:
        model = User
        fields = ['username', 'email']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control', 'id': 'floatingUsername'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address', 'class': 'form-control', 'id': 'floatingEmail'})
        }

    def clean_password2(self):
        cd = self.cleaned_data
        print(cd)
        password1 = cd['password1']
        password2 = cd['password2']
        if password1 != password2:
            raise forms.ValidationError("password")
        else:
            return password1

    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit, *args, **kwargs)
        password = self.cleaned_data['password1']
        instance.set_password(password)
        if commit:
            instance.save()
        return instance

class EnrollmentForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.HiddenInput)