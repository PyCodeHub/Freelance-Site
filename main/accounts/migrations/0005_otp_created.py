# Generated by Django 4.1.7 on 2024-03-07 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_groups_user_is_superuser_user_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
