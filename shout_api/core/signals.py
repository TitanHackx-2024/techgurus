from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Role, UserRole

@receiver(post_save, sender=User)
def assign_default_role(sender, instance, created, **kwargs):
    if created:
        # Determine whether the user should be a Creator or Editor
        if instance.is_editor:
            role_name = 'Editor'
        else:
            role_name = 'Creator'
        
        # Get the appropriate role from the database
        role = Role.objects.get(role_name=role_name)
        
        # Assign the role to the user
        UserRole.objects.create(user=instance, role=role)