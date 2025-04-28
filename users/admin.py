from users.models import User
from django.contrib import admin



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("id", "email", "groups")

