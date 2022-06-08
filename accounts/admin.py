from django.contrib import admin
from .models import User, Farm


class UserAdmin(admin.ModelAdmin):
    list_display = ['surname', 'user_type']


admin.site.register(User, UserAdmin)
admin.site.register(Farm)
