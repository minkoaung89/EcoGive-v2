"""
This module defines the models for the EcoGive application.
In this model, Item represents an item that users can add, share, or inquire about.
"""
from django.db import models
from django.contrib.auth.models import User

#Item model for the items listed by users on EcoGive
class Item(models.Model):
    """Foreign key to link an item to its owner (user)
    CASCADE will ensure if a user is deleted, their items are also will be deleted """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #Title of the item and character limit with 100
    title = models.CharField(max_length=100)
    #Description of the item
    description = models.TextField()

    """Image associated with the item.
    Uploads will be stored in the 'images/' directory"""
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    #Available Quantity for the item; defaults to 1
    quantity = models.PositiveIntegerField(default=1)

    #Automatically set to the current date and time when an item is created
    posted_at = models.DateTimeField(auto_now_add=True)
