# Generated by Django 4.2.16 on 2024-12-02 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluethinkapp', '0012_alter_project_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='timesheet',
            name='custom_project_name',
            field=models.CharField(blank=True, help_text="Enter custom project name if 'Other' is selected", max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='timesheet',
            name='project',
            field=models.CharField(choices=[('Python Training', 'Python Training'), ('On Bench', 'On Bench'), ('Other', 'Other')], default='Python Training', max_length=100),
        ),
    ]
