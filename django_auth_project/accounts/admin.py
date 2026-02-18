from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = [
#         "name",
#         "username",
#         "email", 
#         "is_staff",
#         "phone_number"
#     ]
#     #fieldset hiển thị trong trang EDIT user
#     fieldsets = UserAdmin.fieldsets + (
#         (
#             "UserDetail",
#             {
#                 "fields":
#                 (
#                     "name",
#                     "bio",
#                     "phone_number",
#                 )
#             }
#         ),
#     )
#     #add_fieldsets hiển thị trong trang CREATE user
#     add_fieldsets = UserAdmin.add_fieldsets + (
#         (
#             "UserDetail",
#             {
#                 "fields":
#                 (
#                     "name",
#                     "bio",
#                     "phone_number",
#                 )
#             }
#         ),
#     )
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ("name", "username", "email", "is_staff", "phone_number")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("name", "email", "bio", "phone_number")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "name", "bio", "phone_number", "password1", "password2"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
