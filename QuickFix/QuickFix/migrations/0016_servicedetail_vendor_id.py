# Generated by Django 5.0.7 on 2024-08-27 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuickFix', '0015_servicedetail_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicedetail',
            name='vendor_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
