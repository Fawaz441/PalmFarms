from django.contrib import admin

# Register your models here.
from .models import Channel, Message, TempChatFile

admin.site.register(Channel)
admin.site.register(Message)
admin.site.register(TempChatFile)
