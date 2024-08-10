# Generated by Django 4.0 on 2024-08-10 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postify_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentplatform',
            name='upload_status',
            field=models.CharField(choices=[('queued', 'Queued'), ('failed', 'Failed'), ('success', 'Success')], default='queued', max_length=50),
        ),
        migrations.AlterField(
            model_name='content',
            name='platforms',
            field=models.ManyToManyField(through='postify_app.ContentPlatform', to='postify_app.Platform'),
        ),
    ]
