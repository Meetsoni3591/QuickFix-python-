# Generated by Django 5.0.7 on 2024-09-28 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QuickFix', '0019_alter_servicedetail__new_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicedetail',
            name='_new_price',
        ),
    ]
