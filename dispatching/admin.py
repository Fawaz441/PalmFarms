from django.contrib import admin
from .models import Goods, Dispatch, DispatchAddress, DispatchBreakdown, State

# Register your models here.
admin.site.register(Goods)
admin.site.register(DispatchBreakdown)
admin.site.register(State)
admin.site.register(DispatchAddress)
admin.site.register(Dispatch)
