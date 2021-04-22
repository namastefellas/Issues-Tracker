from django.contrib.auth.models import User
from django import forms
from webapp.models import Project
from accounts.models import Profile
from django.contrib.auth import get_user_model
from django.forms.widgets import PasswordInput



class MyUserCreationForm(forms.ModelForm):
    password = forms.CharField(label="Password", strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Confirm password", required=True, widget=forms.PasswordInput, strip=False)
    email = forms.CharField(label='Email', required=True)

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match!")
        if not first_name and not last_name:
            raise forms.ValidationError("Please, fill one of the fields")


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'last_name', 'email']



class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        exclude = ('user',)


class UserUpdateFrom(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')


class UserChangePasswordForm(forms.ModelForm):
    old_password = forms.CharField(required=True, label='Old password', widget=PasswordInput)
    new_password = forms.CharField(required=True, label='New password', widget=PasswordInput)
    password_confirm = forms.CharField(required=True, label='Password confirmation', widget=PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('old_password', 'new_password', 'password_confirm')

    def clean_password_confirm(self):
        new_password = self.cleaned_data.get('new_password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if new_password != password_confirm:
            raise forms.ValidationError('Password dont match')
        return new_password

    def clean_old_password(self):

        old_password = self.cleaned_data.get('old_password')

        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Password input incorrect')

        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data.get('new_password'))
        if commit:
            user.save()
        return user