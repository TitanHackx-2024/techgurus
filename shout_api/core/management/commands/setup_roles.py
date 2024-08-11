from django.core.management.base import BaseCommand
from core.models import Role, Account

class Command(BaseCommand):
    help = 'Sets up default roles and permissions'

    def handle(self, *args, **kwargs):
        account = Account.objects.get_or_create(account_name='Youtuber')
        admin_role, _ = Role.objects.get_or_create(role_name='Admin')
        admin_role.set_permissions({
            'manage_accounts': True,
            'manage_users': True,
            'manage_content': True,
            'manage_platforms': True,
        })

        creator_role, _ = Role.objects.get_or_create(role_name='Creator')
        creator_role.set_permissions({
            'create_content': True,
            'edit_own_content': True,
            'review_content': True,
        })

        editor_role, _ = Role.objects.get_or_create(role_name='Editor')
        editor_role.set_permissions({
            'edit_assigned_content': True,
            'submit_for_review': True,
        })

        self.stdout.write(self.style.SUCCESS('Successfully set up roles and permissions'))