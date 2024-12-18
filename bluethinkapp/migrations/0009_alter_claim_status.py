# Generated by Django 4.2.16 on 2024-11-28 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluethinkapp', '0008_alter_claim_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], max_length=20, null=True),
        ),
    ]
