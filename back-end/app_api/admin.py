from django.contrib import admin
from django.contrib.auth.models import Group
from .models import TransactionModel, BankModel, VersionsModel, ProfileCollectorModel


class Transaction_admin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'card', 'price', 'date', 'time', 'in_out']
    search_field = ['id', 'date', 'price', 'card', 'in_out']
    ordering = ['-id']

class BankModel_admin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'name', 'stock']
    search_field = ['name']
    ordering = ['-id']

class VersionsModel_admin(admin.ModelAdmin):
    list_display = ['version']
    search_field = ['version']
    ordering = ['-id']

class ProfileCollectorModel_admin(admin.ModelAdmin):
    list_display = ['__str__']
    ordering = ['-id']

admin.site.register(TransactionModel, Transaction_admin)
admin.site.register(BankModel, BankModel_admin)
admin.site.register(VersionsModel, VersionsModel_admin)
admin.site.register(ProfileCollectorModel, ProfileCollectorModel_admin)
admin.site.unregister(Group)