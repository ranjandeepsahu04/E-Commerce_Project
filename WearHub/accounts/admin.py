# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import CustomUser, UserProfile, Address

# class CustomUserAdmin(UserAdmin):
#     list_display = ['username', 'email', 'user_type', 'is_approved', 'is_active']
#     list_filter = ['user_type', 'is_approved', 'is_active']
#     fieldsets = UserAdmin.fieldsets + (
#         ('Additional Info', {'fields': ('user_type', 'phone_number', 'email_verified', 'is_approved')}),
#     )

# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'business_name', 'city', 'state']
#     search_fields = ['user__username', 'business_name']

# class AddressAdmin(admin.ModelAdmin):
#     list_display = ['user', 'full_name', 'city', 'is_default']
#     list_filter = ['is_default', 'city']

# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(Address, AddressAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, Address

class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'is_approved', 'is_active']
    list_filter = ['user_type', 'is_approved', 'is_active']
    actions = ['approve_users']  # Add this line for bulk actions
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'phone_number', 'email_verified', 'is_approved')}),
    )
    
    def approve_users(self, request, queryset):
        """Bulk action to approve selected users"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} user(s) successfully approved.')
    approve_users.short_description = "Approve selected users"

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'business_name', 'city', 'state']
    search_fields = ['user__username', 'business_name']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'city', 'is_default']
    list_filter = ['is_default', 'city']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Address, AddressAdmin)