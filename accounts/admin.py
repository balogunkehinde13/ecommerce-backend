from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# No major customization needed, Django User admin is enough.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
