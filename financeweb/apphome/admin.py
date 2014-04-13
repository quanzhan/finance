from django.contrib import admin
from financeweb.apphome import models
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
class InFinanceAdmin(admin.ModelAdmin):
    list_display = ('startperson', 'maneycount', 'infinancename', 'financeintro','financetype', 'financedate','status')
class FinanceUserAdmin(admin.ModelAdmin):
    list_display = ('finance', 'user', 'status', 'examinedate', 'examineinfo')
class FinanceAdmin(admin.ModelAdmin):
    list_display = ('financename', 'maneycount')

class CashAdmin(admin.ModelAdmin):
    list_display = ('startperson', 'cashname', 'cashintro', 'cashsum','cashtype', 'cashdate')
class UserProfileInline(admin.StackedInline):
    model = models.UserProfile
    verbose_name_plural = 'profile'
class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
admin.site.register(models.InFinance, InFinanceAdmin)
admin.site.register(models.Finance, FinanceAdmin)
admin.site.register(models.FinanceUser, FinanceUserAdmin)
admin.site.register(models.Cash, CashAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
