# campaigns/urls.py
from django.urls import path
from . import views

app_name = "campaigns"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('campaign/<int:campaign_id>/', views.campaign_detail, name='campaign_detail'),
    path('upload_recipients/', views.upload_recipients, name='upload_recipients'),
    path('create_campaign/', views.create_campaign, name='create_campaign'),
]
