from django import forms
from .models import Campaign
import pandas as pd
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'subject', 'content', 'scheduled_time', 'status']
        widgets = {
            'scheduled_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class RecipientUploadForm(forms.Form):
    file = forms.FileField(label="Select CSV or Excel file")

    def clean_file(self):
        file = self.cleaned_data['file']
        valid_extensions = ['.csv', '.xlsx', '.xls']

        if not any(file.name.endswith(ext) for ext in valid_extensions):
            raise forms.ValidationError('Only CSV, XLS, and XLSX files are allowed.')
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:  
                df = pd.read_excel(file)

            if 'email' not in df.columns:
                raise forms.ValidationError("File must have an 'email' column.")

            invalid_emails = []
            for email in df['email']:
                try:
                    validate_email(email)
                except ValidationError:
                    invalid_emails.append(email)

            if invalid_emails:
                raise forms.ValidationError(f"Invalid email addresses: {', '.join(invalid_emails)}")

        except Exception as e:
            raise forms.ValidationError(f"Error reading file: {str(e)}")

        # Reset file pointer after reading
        file.seek(0)
        return file
