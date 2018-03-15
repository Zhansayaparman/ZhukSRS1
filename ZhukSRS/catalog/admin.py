from django.contrib import admin

# Register your models here.

from .models import Konditer, Dami, Tort, Tort_id

#admin.site.register(Tort)
#admin.site.register(Konditer)
# Define the admin class
class KonditersidInline(admin.TabularInline):
    model = Tort

class KonditerAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth')
    inlines = [KonditersidInline]
    fields = ['first_name', 'last_name', ('date_of_birth')]
  
# Register the admin class with the associated model
admin.site.register(Konditer, KonditerAdmin)

admin.site.register(Dami)

class TortsidInline(admin.TabularInline):
    model = Tort_id

@admin.register(Tort)
class TortAdmin(admin.ModelAdmin):
    list_display = ('title', 'konditer', 'display_dami')
    inlines = [TortsidInline]

# Register the Admin classes for BookInstance using the decorator

@admin.register(Tortid)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('tort', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('tort','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )