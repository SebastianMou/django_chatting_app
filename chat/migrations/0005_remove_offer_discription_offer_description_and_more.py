# Generated by Django 4.2.1 on 2023-06-04 17:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0004_offer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='discription',
        ),
        migrations.AddField(
            model_name='offer',
            name='description',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='recipient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='recipient_offer', to=settings.AUTH_USER_MODEL),
        ),
    ]