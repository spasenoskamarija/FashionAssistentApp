
# Register your models here.
from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'dominant_color', 'predicted_style')
    list_filter = ('gender',)
    search_fields = ('user__username', 'dominant_color', 'predicted_style')

admin.site.register(Profile)
