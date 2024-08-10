
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from postify_app.services.uploader_service import get_upload_path

from django.db import connection
from rest_framework.response import Response
from rest_framework import status


from postify_app.models import Account, Content
from postify_app.v1_serialzers import UserRegisterSerializer, LoginSerializer, TokenSerializer, UserReadSerializer, ContentSerializer

class HomeView(APIView):    
    def get(self, request):
        return JsonResponse({"message": "Welcome to the Postify API."})
    
    
class UserRegisterViewV1(APIView):
    serializer_class = UserRegisterSerializer
    
    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    
# login function view for login page
def get_user(request):
    try:
        user = request.session['user_id']
        return user
    except KeyError:
        return None

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    return JsonResponse({
        'authentication': TokenSerializer(user).data,
        'user': UserReadSerializer(user, context={
            'request': request
        }).data,
    }, status=200)
    
        
# Testing 

class HealthCheckView(APIView):
    
    def get(self, request):
        health_status = {
            'database': self.check_database(),
            'auth_token': self.check_auth_token(request),
        }

        if all(health_status.values()):
            return Response({'status': 'healthy', 'details': health_status}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'unhealthy', 'details': health_status}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def check_database(self):
        try:
            connection.ensure_connection()
            return True
        except Exception as e:
            return False

    def check_auth_token(self, request):
        try:
            if request.user and request.auth:
                return True
            return False
        except Exception as e:
            return False 
        
class ContentViewV1(APIView):
    serialzer_class = ContentSerializer
    
    def get(self, request,content_id=None):
        if content_id:
            try:
                content = Content.objects.get(content_id=content_id)
                serializer = self.serialzer_class(content)
                return JsonResponse(serializer.data)
            except Content.DoesNotExist:
                return JsonResponse({'message': 'Content not found.'}, status=404)
        # contents = Content.objects.filter(account_id=request.session.get('account_id'))
        contents = Content.objects.filter(account_id=1)
        serializer = self.serialzer_class(contents, many=True)
        return JsonResponse(serializer.data, safe=False)   
    
    def post(self, request):
        serialzer = self.serialzer_class(data=request.data)
        if serialzer.is_valid():
            serialzer.save()
            return JsonResponse(serialzer.data, status=201, safe=False)
        return JsonResponse(serialzer.errors, status=400) 
        

class ContentUploadViewV1(APIView):
    def post(self, request,content_id):
        res = get_upload_path(request)
        print("res")
        return JsonResponse(res)
