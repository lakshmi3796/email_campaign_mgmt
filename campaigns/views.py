from django.core.paginator import Paginator
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from .models import Campaign
from .forms import CampaignForm,RecipientUploadForm
from .utils import import_recipients_from_file
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard(request):
    qs = Campaign.objects.all().order_by('-created_at')
    paginator = Paginator(qs, 10)
    page = request.GET.get('page')
    campaigns_page = paginator.get_page(page)
    return render(request, 'campaigns/dashboard.html', {'campaigns': campaigns_page})

@staff_member_required
def create_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            if campaign.scheduled_time:
                campaign.status = "scheduled"
            campaign.save()
            messages.success(request, f"Campaign '{campaign.name}' created successfully.")
            return redirect('campaigns:dashboard')
    else:
        form = CampaignForm()
    return render(request, 'campaigns/create_campaign.html', {'form': form})

@staff_member_required
def upload_recipients(request):
    if request.method == 'POST':
        form = RecipientUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            added, skipped = import_recipients_from_file(file)
            messages.success(request, f"{added} recipients added, {skipped} skipped.")
            return redirect('campaigns:upload_recipients')
    else:
        form = RecipientUploadForm()
    return render(request, 'campaigns/upload_recipients.html', {'form': form})

@staff_member_required
def campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    logs = campaign.logs.all().order_by('-sent_at')  
    paginator = Paginator(logs, 25)
    page = request.GET.get('page')
    logs_page = paginator.get_page(page)
    return render(request, 'campaigns/detail.html', {'campaign': campaign, 'logs': logs_page})