"""
Forms for user registration and related functionalities for the EcoGive application.
"""
from django import forms
from django.contrib.auth.models import User

#Custom user registration form
class RegistrationForm(forms.ModelForm):
    """
    A form for registering new users and inheriting fields from the default User model.
    """
    #Minimum length requirement in user password
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=6)

    #Metadata for the form
    class Meta:
        """
        Meta class that specifies the model and fields use in the registration form.
        """
        model = User    #link this form with the built-in User model
        #fields specification from the User model to include in the form
        fields = ['username', 'email', 'password']

    #Custom validation for the username field
    def clean_username(self):
        """
        Validate the username to ensure it meets the minimum character length 
        requirement and uniqueness in the system.
        """
        #Getting the value of the username field
        username = self.cleaned_data.get('username')
        if len(username) < 3:   #minimum length requirement in username
            raise forms.ValidationError("Username must be at least 3 characters long.")
        #Check if the username already exists in the system
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken. Please choose a different one.")
        return username

    #Custom validation for the email field
    def clean_email(self):
        """
        Validate the email to ensure uniqueness in the system.
        """
        #Getting the value of the email field
        email = self.cleaned_data.get('email')
        #check if the email already exists in the system
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Email is already registered. Please use a different email.")
        return email

    #Overall form validation
    def clean(self):
        #Call the parent class's clean method to get the cleaned data
        cleaned_data = super().clean()
        password = cleaned_data.get("password") #Get the cleaned password
        confirm_password = cleaned_data.get("confirm_password")
        #Password validation with confirm password
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
