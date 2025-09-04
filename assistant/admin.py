
# Register your models here.
from django.contrib import admin
from .models import Profile, ClothingItem, UserOutfit, OutfitPlan

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'dominant_color', 'predicted_style')
    list_filter = ('gender',)
    search_fields = ('user__username',)

admin.site.register(ClothingItem)
admin.site.register(UserOutfit)
admin.site.register(OutfitPlan)

