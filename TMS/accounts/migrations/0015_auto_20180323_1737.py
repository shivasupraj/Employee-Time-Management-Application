# Generated by Django 2.0.3 on 2018-03-23 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_timesheet_emp_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timesheet',
            old_name='employees',
            new_name='profile',
        ),
    ]