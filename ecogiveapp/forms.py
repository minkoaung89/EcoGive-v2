from django import forms
from django.contrib.auth.models import User

#Custom user registration form
class RegistrationForm(forms.ModelForm):
    #Minimum length requirement in user password
    password = forms.CharField(widget=forms.PasswordInput, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=6)

    #Metadata for the form
    class Meta:
        model = User    #link this form with the built-in User model
        fields = ['username', 'email', 'password']  #fields specification from the User model to include in the form
        
    #Custom validation for the username field
    def clean_username(self):
        username = self.cleaned_data.get('username')    #Getting the value of the username field
        if len(username) < 3:   #minimum length requirement in username
            raise forms.ValidationError("Username must be at least 3 characters long.")
        if User.objects.filter(username=username).exists(): #Check if the username already exists in the system
            raise forms.ValidationError("Username is already taken. Please choose a different one.")
        return username

    #Custom validation for the email field
    def clean_email(self):  
        email = self.cleaned_data.get('email')  #Getting the value of the email field
        if User.objects.filter(email=email).exists():   #check if the email already exists in the system
            raise forms.ValidationError("Email is already registered. Please use a different email.")
        return email

    #Overall form validation
    def clean(self):
        cleaned_data = super().clean()  #Call the parent class's clean method to get the cleaned data
        password = cleaned_data.get("password") #Get the cleaned password
        confirm_password = cleaned_data.get("confirm_password") 
        
        #Password validation with confirm password
        if password != confirm_password:    
            raise forms.ValidationError("Passwords do not match.")
