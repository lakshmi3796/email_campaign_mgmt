# campaigns/models.py
from django.db import models

class Recipient(models.Model):
    SUBSCRIBED = 'sub'
    UNSUBSCRIBED = 'unsub'
    STATUS_CHOICES = [(SUBSCRIBED, 'Subscribed'), (UNSUBSCRIBED, 'Unsubscribed')]
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=SUBSCRIBED)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Campaign(models.Model):
    STATUS_CHOICES = [('draft', 'Draft'), ('scheduled', 'Scheduled'),
                      ('in_progress', 'In Progress'), ('completed', 'Completed')]
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    scheduled_time = models.DateTimeField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)

    def total_recipients(self):
        return Recipient.objects.filter(status=Recipient.SUBSCRIBED).count()

    def sent_count(self):
        return self.logs.filter(status=EmailLog.STATUS_SENT).count()

    def failed_count(self):
        return self.logs.filter(status=EmailLog.STATUS_FAILED).count()

    def __str__(self):
        return self.name


class EmailLog(models.Model):
    STATUS_SENT = 'sent'
    STATUS_FAILED = 'failed'
    STATUS_CHOICES = [(STATUS_SENT, 'Sent'), (STATUS_FAILED, 'Failed')]
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='logs')
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    status = models.CharField(max_length=6, choices=STATUS_CHOICES)
    failure_reason = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient.email} - {self.status}"

