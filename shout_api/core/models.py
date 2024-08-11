from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
import json

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
    account_status = models.CharField(max_length=50, choices=AccountStatus.choices, default=AccountStatus.ACTIVE)

    def __str__(self):
        return f"{self.account_name} - {self.account_id}"

class User(AbstractUser, AuditedModel):
    class UserStatus(models.TextChoices):
        ACTIVE = 'active'
        INACTIVE = 'inactive'
    
    user_status = models.CharField(max_length=50, choices=UserStatus.choices, default=UserStatus.ACTIVE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE,  null=True, blank=True)
    phone_number = models.CharField(max_length=255, blank=True)
    is_editor = models.BooleanField(default=False)


    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="custom_user_set",
        related_query_name="custom_user",
    )

    class Meta:
        unique_together = (('email', 'account'),)

    def assign_role(self, role_name):
        role, created = Role.objects.get_or_create(role_name=role_name)
        UserRole.objects.get_or_create(user=self, role=role)

    def remove_role(self, role_name):
        UserRole.objects.filter(user=self, role__role_name=role_name).delete()

    def has_role(self, role_name):
        return self.userrole_set.filter(role__role_name=role_name).exists()

    def __str__(self):
        return f"{self.email} - {self.account if self.account else 'No Account'}"




class Role(models.Model):
    role_name = models.CharField(max_length=255)
    permissions = models.TextField(default='{}')

    def get_permissions(self):
        return json.loads(self.permissions)

    def set_permissions(self, permissions):
        self.permissions = json.dumps(permissions)
        self.save()

    def has_permission(self, permission_key):
        permissions = self.get_permissions()
        return permissions.get(permission_key, False)

    def __str__(self):
        return self.role_name

class UserRole(AuditedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

class Platform(models.Model):
    PLATFORM_CHOICES = [
        ('youtube', 'YouTube'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter'),
        ('tiktok', 'TikTok'),
        ('facebook', 'Facebook'),
        ('spotify', 'Spotify'),
        ('linkedin', 'LinkedIn'),
    ]

    name = models.CharField(max_length=50, choices=PLATFORM_CHOICES, unique=True)

    def __str__(self):
        return f"{self.name} - {self.id}"



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
        IN_PROGRESS = 'in_progress'
        REJECTED = 'rejected'
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    text_content = models.TextField(blank=True)
    raw_content = models.FileField(upload_to='raw_content/', blank=True, null=True)
    edited_content = models.FileField(upload_to='edited_content/', blank=True, null=True)
    content_type = models.CharField(max_length=50, choices=ContentType.choices)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_content')
    editor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='edited_content')
    scheduled_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=ContentStatus.choices, default=ContentStatus.DRAFT)
    platforms = models.ManyToManyField(Platform, through='ContentPlatform')

    def assign_editor(self, editor):
        self.editor = editor
        self.status = self.ContentStatus.IN_PROGRESS
        self.save()

    def submit_for_review(self):
        self.status = self.ContentStatus.IN_REVIEW
        self.save()

    def approve(self):
        self.status = self.ContentStatus.APPROVED
        self.save()

    def reject(self):
        self.status = self.ContentStatus.REJECTED
        self.save()
    
    def __str__(self):
        return f"{self.title} - {self.id}"

class ContentPlatform(models.Model):
    class UploadStatus(models.TextChoices):
        QUEUED = 'queued'
        FAILED = 'failed'
        SUCCESS = 'success'
        
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    upload_status = models.CharField(max_length=50, choices=UploadStatus.choices, default=UploadStatus.QUEUED)

    class Meta:
        unique_together = ('content', 'platform')