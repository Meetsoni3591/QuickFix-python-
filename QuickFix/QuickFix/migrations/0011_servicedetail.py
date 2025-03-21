# Generated by Django 5.0.7 on 2024-08-18 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuickFix', '0010_vendorreg'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=100)),
                ('area', models.CharField(max_length=100)),
                ('avilable', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('experience', models.CharField(max_length=100)),
                ('service_warranty', models.CharField(max_length=100)),
                ('desc', models.CharField(max_length=250)),
                ('service_image', models.ImageField(max_length=250, upload_to='images/')),
                ('certificate', models.ImageField(max_length=250, upload_to='images/')),
            ],
        ),
    ]
