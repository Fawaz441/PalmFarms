from django.contrib import admin
from .models import User, Farm, FAQ, ContactMessage, NewsLetterMember


class UserAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'user_type', 'phone_number']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone_no',
                    'first_name', 'last_name', 'message']


admin.site.register(User, UserAdmin)
admin.site.register(Farm)
admin.site.register(FAQ)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(NewsLetterMember)
