from django import forms
from django.contrib.auth import get_user_model, forms as auth_forms

User = get_user_model()


class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email']

    error_messages = {
        'email_already_exists': 'A user with this email already exists.',
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.error_messages['email_already_exists'])
        return email


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email']
