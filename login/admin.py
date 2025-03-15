from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    fields = ('school',)


class UserAdminPanel(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active', 'get_school')
    search_fields = ('username', 'email', 'profile__school__name')
    list_filter = ('is_staff', 'is_active')
    inlines = [ProfileInline]  # Embed Profile form inside User form

    def get_school(self, obj):
        """Show school in User list display."""
        return obj.profile.school if hasattr(obj, 'profile') and obj.profile.school else "N/A"
    get_school.short_description = 'School'  # Column header name


@admin.register(Profile)
class ProfileAdminPanel(admin.ModelAdmin):
    list_display = ('user', 'school')
    search_fields = ('user__username', 'user__email', 'school__name')
    list_filter = ('school',)

# Unregister the default User admin panel and register the customized one:
admin.site.unregister(User)
admin.site.register(User, UserAdminPanel)