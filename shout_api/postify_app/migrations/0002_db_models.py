from django.db import migrations
import json

def create_default_roles(apps, schema_editor):
    Role = apps.get_model('postify_app', 'Role')
    
    roles = [
        ('readonlyuser', {"view": True, "edit": False, "upload": False}),
        ('editor', {"view": True, "edit": True, "upload": False}),
        ('admin', {"view": True, "edit": True, "upload": True}),
    ]
    
    for role_name, permissions in roles:
        if not Role.objects.filter(role_name=role_name).exists():
            Role.objects.create(
                role_name=role_name,
                permissions=json.dumps(permissions) 
            )

def undo_create_default_roles(apps, schema_editor):
    Role = apps.get_model('postify_app', 'Role')
    role_names = ['readonlyuser', 'editor', 'admin']
    Role.objects.filter(role_name__in=role_names).delete()
    
def create_default_platforms(apps, schema_editor):
    Platform = apps.get_model('postify_app', 'Platform')
    platforms = [
        'youtube',
        'instagram',
        'twitter',
        'tiktok',
        'facebook',
        'spotify',
        'linkedin',
    ]
    for platform_name in platforms:
        if not Platform.objects.filter(ui_mapping_name=platform_name).exists():
            Platform.objects.create(ui_mapping_name=platform_name)

def undo_create_default_platforms(apps, schema_editor):
    Platform = apps.get_model('postify_app', 'Platform')
    
    platforms = [
        'youtube',
        'instagram',
        'twitter',
        'tiktok',
        'facebook',
        'spotify',
        'linkedin',
    ]
    
    Platform.objects.filter(ui_mapping_name__in=platforms).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('postify_app', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_default_roles, undo_create_default_roles),
        migrations.RunPython(create_default_platforms, undo_create_default_platforms),
    ]
