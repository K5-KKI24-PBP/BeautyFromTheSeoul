from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    user_role = forms.ChoiceField(
        choices= (("admin", "Admin"), ("customer", "Customer")),
        label= "User Role: ",
        required= True,
        )
    email= forms.EmailField(label= "Enter your Email Address", required= True)
    name= forms.CharField(label= "Enter your Name", required= True)

    class Meta:
        model= User
        fields= ['username', 'name', 'email', 'password1', 'password2', 'user_role']

    def save(self, commit= True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['name']
        user_role = self.cleaned_data['user_role']
        
        if user_role == "admin":
            user.is_superuser = True
            user.is_staff = True
        
        if user_role == "customer":
            user.is_superuser = False
            user.is_staff = False

        if commit:
            user.save()
            UserProfile.objects.create(user=user, user_role=user_role)
        
        return user