# Generated by Django 5.0.7 on 2024-07-22 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuickFix', '0007_remove_userdata_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
