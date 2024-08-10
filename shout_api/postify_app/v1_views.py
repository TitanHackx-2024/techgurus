from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404



from postify_app.models import Account, Content
from postify_app.v1_serialzers import UserRegisterSerializer

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
    if request.method == 'POST':
        email_address = request.data.get('email_address')
        password = request.data.get('password')
        account_id = request.session.get('account_id')
        
        account = get_object_or_404(Account,account_id=account_id)
        if account.user_set.filter(email_address=email_address).exists():
            user = account.user_set.get(email_address=email_address)
            if user.password_hash == password:
                return JsonResponse({'message': 'User logged in successfully.','user_id': user.user_id})
            else:
                return JsonResponse({'message': 'Invalid password.'})
        else:
            return JsonResponse({'message': 'User does not exist.'})
        
