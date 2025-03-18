# Generated by Django 5.0.7 on 2024-11-02 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QuickFix', '0020_remove_servicedetail__new_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('area', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.CharField(max_length=255)),
                ('apartment_suite', models.CharField(max_length=255)),
                ('landmark', models.CharField(max_length=100)),
                ('postal_zip', models.CharField(max_length=6)),
                ('service_category', models.CharField(max_length=100)),
                ('service_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('service_area', models.CharField(max_length=50)),
                ('service_email', models.CharField(max_length=100)),
            ],
        ),
    ]
