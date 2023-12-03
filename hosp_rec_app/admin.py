from django.contrib import admin
from .models import Hospital,UserResponse,Schedule,Preference
from django.contrib.postgres.fields import ArrayField
# Register your models here.

admin.site.register(UserResponse)
admin.site.register(Schedule)
admin.site.register(Preference)
admin.site.register(Hospital)



