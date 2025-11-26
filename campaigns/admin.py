# campaigns/admin.py
from django.contrib import admin
from .models import Campaign, Recipient, EmailLog

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'scheduled_time', 'status')

@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'status')

@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'recipient', 'status', 'failure_reason', 'sent_at')
