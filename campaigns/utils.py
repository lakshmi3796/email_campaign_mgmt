import csv
from io import StringIO
from django.core.mail import EmailMessage

import pandas as pd
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from campaigns.models import Recipient

def import_recipients_from_file(file):
    added = 0
    skipped = 0
    if file.name.endswith('.csv'):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    if 'email' not in df.columns:
        raise ValueError("File must have an 'email' column.")

    name_col = 'name' if 'name' in df.columns else None

    for idx, row in df.iterrows():
        email = str(row['email']).strip()
        name = str(row[name_col]).strip() if name_col else email.split('@')[0]

        try:
            validate_email(email)
        except ValidationError:
            skipped += 1
            continue

        # Skip duplicates
        if Recipient.objects.filter(email=email).exists():
            skipped += 1
            continue

        # Add recipient
        Recipient.objects.create(
            name=name,
            email=email,
            status=Recipient.SUBSCRIBED
        )
        added += 1

    return added, skipped

def generate_report(campaign):
    logs = campaign.logs.all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Recipient', 'Status', 'Failure Reason'])
    for log in logs:
        writer.writerow([log.recipient.email, log.status, log.failure_reason or "--"])
    # send to admin
    email = EmailMessage(
        subject=f"Campaign Report - {campaign.name}",
        body="Attached report",
        from_email='lakshmipatel371996@gmail.com',
        to=['lakshmipatel371996@gmail.com'],
    )
    email.content_subtype = "html"
    email.attach(f'{campaign.name}_report.csv', output.getvalue(), 'text/csv')
    email.send()
