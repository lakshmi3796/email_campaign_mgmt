from django.core.mail import EmailMessage
from .models import Campaign, Recipient, EmailLog
from concurrent.futures import ThreadPoolExecutor
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bulk_email_system.settings")
django.setup()

def send_email_to_recipient(campaign, recipient):
    try:
        print(campaign.content)
        print(recipient.email)
        email = EmailMessage(
            subject=campaign.subject,
            body=campaign.content,
            from_email='lakshmipatel371996@gmail.com',
            to=[recipient.email],
        )
        email.content_subtype = "html"
        email.send(fail_silently=False)

        # Log success
        EmailLog.objects.create(
            campaign=campaign,
            recipient=recipient,
            status='sent'
        )
    except Exception as e:
        EmailLog.objects.create(
            campaign=campaign,
            recipient=recipient,
            status='failed',
            failure_reason=str(e)
        )

def run_campaign(campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    campaign.status = 'in_progress'
    campaign.save()
    recipients = Recipient.objects.filter(status=Recipient.SUBSCRIBED)
    with ThreadPoolExecutor(max_workers=10) as executor:
        for recipient in recipients:
            executor.submit(send_email_to_recipient, campaign, recipient)
    campaign.status = 'completed'
    campaign.save()
