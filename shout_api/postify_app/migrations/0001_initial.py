# Generated by Django 5.1 on 2024-08-10 07:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('account_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('account_name', models.CharField(max_length=255)),
                ('account_status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('platform_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('platform_name', models.CharField(choices=[('youtube', 'Youtube'), ('instagram', 'Instagram'), ('twitter', 'Twitter'), ('tiktok', 'Tiktok'), ('facebook', 'Facebook'), ('spotify', 'Spotify'), ('linkedin', 'Linkedin')], default='youtube', max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('role_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=255)),
                ('permissions', models.TextField(default='{}')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('content_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('file_path', models.CharField(max_length=255)),
                ('content_type', models.CharField(choices=[('Video', 'Video'), ('Image', 'Image'), ('Text', 'Text'), ('Audio', 'Audio')], default='Text', max_length=50)),
                ('scheduled_time', models.DateTimeField(blank=True, null=True)),
                ('upload_status', models.CharField(choices=[('draft', 'Draft'), ('in_review', 'In Review'), ('approved', 'Approved')], default='draft', max_length=50)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postify_app.account')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContentPlatform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postify_app.content')),
                ('platform_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postify_app.platform')),
            ],
            options={
                'unique_together': {('content_id', 'platform_id')},
            },
        ),
        migrations.AddField(
            model_name='content',
            name='platforms',
            field=models.ManyToManyField(through='postify_app.ContentPlatform', to='postify_app.platform'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_name', models.CharField(max_length=255)),
                ('user_status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=50)),
                ('password_hash', models.CharField(max_length=255)),
                ('email_address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postify_app.account')),
            ],
            options={
                'unique_together': {('email_address', 'account_id')},
            },
        ),
        migrations.AddField(
            model_name='content',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postify_app.user'),
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postify_app.role')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postify_app.user')),
            ],
            options={
                'unique_together': {('user_id', 'role_id')},
            },
        ),
    ]
