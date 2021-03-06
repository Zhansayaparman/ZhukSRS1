﻿from django.db import models
from django.contrib.auth.models import User

class Dami( models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction).
    """
    name = models.CharField(max_length=200, help_text="Дәмін таңдаңыз")
    
    
    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Tort(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    konditer = models.ForeignKey('Konditer', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, help_text=' Қандай торт екенін жазыңыз ')
    isbn = models.CharField('ISBN',max_length=15, help_text='15 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    dami = models.ManyToManyField(Dami, help_text='Торттың дәмән таңдаңыз ')
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    
   
    def display_dami(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ dami.name for dami in self.dami.all()[:3] ])
	
    display_dami().short_description = 'Dami'
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title
		
    def get_absolute_url(self):
        """
        Returns the url to access a detail record for this book.
        """
        return reverse('tort-detail', args=[str(self.id)])

import uuid # Required for unique book instances

class Tort_id(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    tort = models.ForeignKey('Tort', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Tort availability')

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)
        

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{0} ({1})'.format(self.id,self.tort.title)
class Konditer(((models.Model))):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)


    class Meta:
        ordering = ["last_name","first_name"]
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('konditer-detail', args=[str(self.id)])
    

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0}, {1}'.format(self.last_name,self.first_name)
   