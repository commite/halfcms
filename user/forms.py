from django import forms
from .models import User
from django.utils.translation import ugettext_lazy as _


class SignUpForm(forms.ModelForm):
    error_message = {
        'password_mismatch': _("Sorry, password fields don´t match.",)
    }
    password2 = forms.CharField(
                                label='Password confirmation',
                                widget=forms.PasswordInput
                                )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError(
                self.error_message['password_mismatch'],
                code='password_mismatch',
            )
            return password2

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user
