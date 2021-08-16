from django.contrib import admin
from .models import UserLoginActivity
# Register your models here.

def download_csv(modeladmin, request, queryset):
    import csv
    f = open('./history.csv', 'w')
    writer = csv.writer(f)
    writer.writerow(['login_IP', 'status', 'user_agent_info','login_username'])
    for s in queryset:
        writer.writerow([s.login_IP, s.status, s.user_agent_info, s.login_username])

@admin.register(UserLoginActivity)
class UserLoginActivityAdmin(admin.ModelAdmin):
    list_display = ['login_IP', 'status', 'user_agent_info','login_username']
    actions = [download_csv]