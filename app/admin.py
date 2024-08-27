from django.contrib import admin
from .models import CustomUser, ClassifiedAd

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ['email', 'name', 'is_active', 'is_staff']
    search_fields = ['email', 'name']

class ClassifiedAdAdmin(admin.ModelAdmin):
    model = ClassifiedAd
    list_display = ['title', 'price', 'category', 'user']
    search_fields = ['title', 'category']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ClassifiedAd, ClassifiedAdAdmin)
