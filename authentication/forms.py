from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
        user= super(RegistrationForm, self).save(commit= False)
        if commit:
            user.save()

        return user
    