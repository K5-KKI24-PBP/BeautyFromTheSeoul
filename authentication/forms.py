from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError 

class RegistrationForm(UserCreationForm):
    user_role = forms.ChoiceField(
        choices=(("admin", "Admin"), ("customer", "Customer")),
        label="User Role: ",
        required=True,
        widget=forms.Select(attrs={"class": "form-select"})  # Dropdown style
    )
    email = forms.EmailField(
        label="Enter your Email Address",
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "name@example.com"})
    )
    name = forms.CharField(
        label="Enter your Name",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Full Name"})
    )

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password1', 'password2', 'user_role']
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            'password1': forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}),
            'password2': forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm Password"}),
        }

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # Apply form-control to password fields if not applied by Meta
        self.fields['password1'].widget.attrs.update({"class": "form-control", "placeholder": "Password"})
        self.fields['password2'].widget.attrs.update({"class": "form-control", "placeholder": "Confirm Password"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name']
        user_role = self.cleaned_data['user_role']
        
        # Set permissions based on role
        if user_role == "admin":
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False

        if commit:
            user.save()
            # Create an associated UserProfile with the selected role
            UserProfile.objects.create(user=user, user_role=user_role)
        
        return user

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Password'
        })
    )
