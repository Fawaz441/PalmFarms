from django.contrib import admin
from .models import Consultant, ConsultantFile, ConsultingRequest
admin.site.register(Consultant)
admin.site.register(ConsultantFile)
admin.site.register(ConsultingRequest)
