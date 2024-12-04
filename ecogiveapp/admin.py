""" A file automatically created in each Django project. """

from django.contrib import admin

#Import the Item model to admin
from .models import Item

#Register the Item model to be accessible through the admin interface.
admin.site.register(Item)
