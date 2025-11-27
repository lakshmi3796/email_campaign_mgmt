# scripts/send_campaigns.py

from django.utils import timezone
from campaigns.models import Campaign
from campaigns.email_sender import run_campaign
from campaigns.utils import generate_report

def run():
    now = timezone.now()
    campaigns = Campaign.objects.filter(status='scheduled',scheduled_time__lte=now)
    for campaign in campaigns:
        run_campaign(campaign.id)
        print(f"Campaign '{campaign.name}' sent at {timezone.now()}")
        generate_report(campaign)
    
