from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


from core.models import Content
from core.serializers.contents import ContentSerializer, ContentCreateSerializer
from core.permissions import HasRolePermission, IsContentCreator, IsEditor
from core.services.uploader_service import UploaderService

from django.contrib.auth import get_user_model

User = get_user_model()


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    permission_classes = [permissions.IsAuthenticated, HasRolePermission]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'content_type']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'scheduled_time']

    def get_serializer_class(self):
        if self.action == 'create':
            return ContentCreateSerializer
        return ContentSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.has_role('Admin'):
            return Content.objects.filter(account=None)
        elif user.has_role('Editor'):
            return Content.objects.filter(account=None, editor=user)
        else:
            return Content.objects.filter(account=user.account, created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, account=self.request.user.account)


    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsContentCreator | HasRolePermission])
    def assign_editor(self, request, pk=None):
        content = self.get_object()
        editor_id = request.data.get('editor_id')
        if editor_id:
            try:
                editor = User.objects.get(id=editor_id)
                if editor.has_role('Editor'):
                    content.assign_editor(editor)
                    return Response({'status': 'Editor assigned successfully'})
                else:
                    return Response({'error': 'User is not a editor'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'error': 'Editor not found'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Editor ID not provided'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsEditor])
    def submit_for_review(self, request, pk=None):
        content = Content.objects.filter(id=pk, editor=self.request.user).first()
        edited_content = request.FILES.get('edited_content')
        if edited_content:
            content.edited_content = edited_content
            content.save()

        content.submit_for_review()
        return Response({'status': 'Content submitted for review'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsContentCreator | HasRolePermission])
    def approve(self, request, pk=None):
        content = self.get_object()
        content.approve()
        return Response({'status': 'Content approved'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsContentCreator | HasRolePermission])
    def reject(self, request, pk=None):
        content = self.get_object()
        content.reject()
        return Response({'status': 'Content rejected'})
    

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated, IsContentCreator | HasRolePermission])
    def publish(self, request, pk=None):
        content = self.get_object()
        print(content)

        success_platforms , failed_platforms = UploaderService.upload_to_platforms(content)
        
        if len(success_platforms) == 0:
            return Response('Failed to upload content to all platforms.')
            
        content.status = Content.ContentStatus.PUBLISHED
        content.save()

        return Response({'status': f'Published content: {content.title}'})
    

    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAuthenticated, IsContentCreator | HasRolePermission]
        elif self.action in ['list', 'retrieve', 'assign_editor', 'approve', 'reject']:
            self.permission_classes = [permissions.IsAuthenticated, HasRolePermission | IsContentCreator]
        elif self.action == 'submit_for_review':
            self.permission_classes = [permissions.IsAuthenticated, IsEditor]
        return super().get_permissions()