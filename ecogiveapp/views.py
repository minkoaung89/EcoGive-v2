from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError  
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .models import Item
from .forms import RegistrationForm

#For User Registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)   #Use the custom registrationform from forms.spy
        if form.is_valid():
            password = form.cleaned_data.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password != confirm_password:
                form.add_error('confirm_password', 'Passwords do not match.')
            else:
                try:
                    #Validate the password using Django's built-in validators
                    validate_password(password)

                    #Save the user to system if password is valid
                    user = form.save(commit=False)
                    user.set_password(password)
                    user.save()

                    messages.success(request, "Registration successful! Please log in.")
                    return redirect('login')

                except ValidationError as e:
                    form.add_error('password', e)   #Handle password validation errors

        else:
            #If form is not valid, show error messages
            messages.error(request, "There were some errors in the form. Please correct them.")
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

#For User login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')  #Redirect to the user dashboard after login
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')

#For User logout
def user_logout(request):
    logout(request)
    return redirect('login')

#For adding an item
@login_required #User need to login first to add new item
def add_item(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        quantity = request.POST['quantity']
        image = request.FILES.get('image')  #Get the uploaded image

        if not image:
            messages.error(request, "Image is required.")
            return render(request, 'add_item.html')

        try:
            item = Item.objects.create( #Create and save the new item
                title=title,
                description=description,
                quantity=quantity,
                image=image,  #Save the image field
                owner=request.user
            )
            messages.success(request, 'Item added successfully!')
            return redirect('dashboard')
        except Exception as e:  #Handle exceptions while adding an item
            messages.error(request, f'Error adding item: {e}')
    
    return render(request, 'add_item.html')

#For Editing an Item
@login_required #Only authenticated users to edit their existing item
def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, owner=request.user)
    if request.method == 'POST':
        item.title = request.POST['title']
        item.description = request.POST['description']
        item.quantity = request.POST['quantity']

        #Handling the image replacement
        if 'image' in request.FILES:
            if item.image:
                #Delete the old image from S3 before updating
                item.image.delete(save=False)
            item.image = request.FILES['image']

        item.save()
        
        #Add a success message and redirect to avoid form resubmission
        messages.success(request, 'Item updated successfully!')
        return redirect('dashboard')
    
    return render(request, 'edit_item.html', {'item': item})


#For Deleting an Item
@login_required
def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id, owner=request.user)
    if request.method == 'POST':
        #Delete the image from S3 before deleting the item
        if item.image:
            item.image.delete(save=False)
        item.delete()
        messages.success(request, 'Item deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'delete_item.html', {'item': item})
    
#For item inquiry
def inquire_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == 'POST':
        email = request.POST.get('email').strip()  # Get the user's email from the form
        message = request.POST.get('message').strip()

        #Check if email is valid
        if not email:
            messages.error(request, "Email is required to send an inquiry.")
            return render(request, 'inquire_item.html', {'item': item})
        
        #Prepare the email message content
        inquiry_message = f"""
        You have new inquiry as below.
        
        Message:
        {message}
        """

        try:
            #Create an email message with reply-to header
            email_message = EmailMessage(
                subject=f'Inquiry about {item.title}',
                body=inquiry_message,
                from_email=settings.DEFAULT_FROM_EMAIL,  #Use the default sender email from settings.py
                to=[item.owner.email],  #Send to item owner
                reply_to=[email],  #Set reply-to to the user's email
            )
            email_message.send(fail_silently=False)

            messages.success(request, 'Inquiry sent successfully.')
        except Exception as e:
            #detailed error message for debugging
            print("Error while sending email:", e)
            messages.error(request, f'Error sending inquiry: {e}')
        return redirect('item_list')

    return render(request, 'inquire_item.html', {'item': item})

#For home page view
def home(request):
    query = request.GET.get('query', '')
    if query:   #filtered items based on a search query
        items = Item.objects.filter(title__icontains=query).order_by('-posted_at')
    else:   #Displays the home page with all items
        items = Item.objects.all().order_by('-posted_at')

    return render(request, 'home.html', {'items': items})

#For item list view
def item_list(request):
    #Check if query parameter "all=true" is set to show all items
    all_items = request.GET.get('all', 'false').lower() == 'true'

    if all_items or not request.user.is_authenticated:
        items = Item.objects.all().order_by('-posted_at')  #Show all items for public users
    else:
        items = Item.objects.filter(owner=request.user).order_by('-posted_at')  #Show only the logged-in user's items

    return render(request, 'item_list.html', {'items': items})


#Dashboard for registered users
@login_required
def dashboard(request):
    user_items = Item.objects.filter(owner=request.user).order_by('-posted_at')  #Show only items owned by logged-in user
    return render(request, 'dashboard.html', {'items': user_items})
    
#View Item Detail Displays for an individual item
def view_item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item_detail.html', {'item': item})
