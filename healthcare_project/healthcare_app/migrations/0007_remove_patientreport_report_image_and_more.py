# Generated by Django 5.1.7 on 2025-03-10 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare_app', '0006_patientreport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientreport',
            name='report_image',
        ),
        migrations.AlterField(
            model_name='patientreport',
            name='report_pdf',
            field=models.FileField(upload_to='reports/pdfs/'),
        ),
    ]
