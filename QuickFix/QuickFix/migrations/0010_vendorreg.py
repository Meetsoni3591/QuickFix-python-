# Generated by Django 5.0.7 on 2024-08-10 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuickFix', '0009_delete_userdata2_alter_contactus_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorReg',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
