from django.db import models
import json

# base model 
class AuditedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        
class Account(AuditedModel):
    class AccountStatus(models.TextChoices):
        ACTIVE = 'active'
        INACTIVE = 'inactive'
    account_id = models.BigAutoField(primary_key=True)
    account_name = models.CharField(max_length=255)
    account_status = models.CharField(max_length=50,choices=AccountStatus.choices, default=AccountStatus.ACTIVE)
    
    def __str__(self):
        return str(self.account_name)
    
class User(AuditedModel):
    class Meta:
        unique_together = (('email_address', 'account_id'),)
    class UserStatus(models.TextChoices):
        ACTIVE = 'active'
        INACTIVE = 'inactive'
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    user_status = models.CharField(max_length=50,choices=UserStatus.choices, default=UserStatus.ACTIVE)
    password_hash = models.CharField(max_length=255)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    email_address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    
    
    def __str__(self):
        return self.user_name
    
class Role(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=255)
    permissions = models.TextField(default='{}')  # Store JSON as a string
    
    def get_permissions(self):
        return json.loads(self.permissions)

    def set_permissions(self, permissions):
        self.permissions = json.dumps(permissions)
        self.save()
        
    def has_permission(self, permission_key):
        permissions = self.get_permissions()
        return permissions.get(permission_key, False)
    
class UserRole(AuditedModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user_id', 'role_id')
        
class Platform(AuditedModel):
    class DefaultPlatform(models.TextChoices):
        YOUTUBE = 'youtube'
        INSTAGRAM = 'instagram'
        TWITTER = 'twitter'
        TIKTOK = 'tiktok'
        FACEBOOK = 'facebook'
        SPOTIFY = 'spotify'
        LINKEDIN = 'linkedin'
        
    platform_id = models.BigAutoField(primary_key=True)
    platform_name = models.CharField(max_length=255, choices=DefaultPlatform.choices, default=DefaultPlatform.YOUTUBE)

class ContentPlatform(models.Model):
    class Meta:
        unique_together = ('content_id', 'platform_id')
    content_id = models.ForeignKey('Content', on_delete=models.CASCADE)
    platform_id = models.ForeignKey('Platform', on_delete=models.CASCADE)


class Content(AuditedModel):
    class ContentType(models.TextChoices):
        VIDEO = 'Video'
        IMAGE = 'Image'
        TEXT = 'Text'
        AUDIO = 'Audio'
    class ContentStatus(models.TextChoices):
        DRAFT = 'draft'
        IN_REVIEW = 'in_review'
        APPROVED = 'approved'    
    
    content_id = models.BigAutoField(primary_key=True)
    account_id = models.ForeignKey('Account', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file_path = models.CharField(max_length=255)
    content_type = models.CharField(max_length=50, choices=ContentType.choices, default=ContentType.TEXT)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField(null=True, blank=True) 
    upload_status = models.CharField(max_length=50, choices=ContentStatus.choices, default=ContentStatus.DRAFT)
    platforms = models.ManyToManyField('Platform', through='ContentPlatform') 