# Generated by Django 5.1.3 on 2024-12-14 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_role_customuser_roles'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='name',
        ),
        migrations.AddField(
            model_name='author',
            name='first_name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='author',
            name='last_name',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='preview_image',
            field=models.ImageField(blank=True, null=True, upload_to='videos/previews/'),
        ),
    ]
