from enum import Enum
from django.conf import settings
from postify_app.models import Account


def get_upload_path(request):
    account_id = Account.objects.get(account_id=1)
    print("account_id",account_id)
    return 'Testing'