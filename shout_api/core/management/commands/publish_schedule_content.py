from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Content
from core.services.uploader_service import UploaderService

class Command(BaseCommand):
    help = 'Publishes scheduled content'

    def handle(self, *args, **options):
        now = timezone.now()
        scheduled_content = Content.objects.filter(
            status=Content.ContentStatus.APPROVED,
            scheduled_time__lte=now
        )
        
        for content in scheduled_content:
            
            success_platforms , failed_platforms = UploaderService.upload_to_platforms(content)
        
            if len(success_platforms) == 0:
                self.stdout.errors(self.style.ERROR('Failed to upload content to all platforms.'))
                
            content.status = Content.ContentStatus.PUBLISHED
            content.save()
            self.stdout.write(self.style.SUCCESS(f'Published content: {content.title}'))

        self.stdout.write(self.style.SUCCESS('Finished publishing scheduled content'))