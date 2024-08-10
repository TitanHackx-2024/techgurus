from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView

# Create your views here.
class HomeView(APIView):    
    def get(self, request):
        return JsonResponse({"message": "Welcome to the Postify API."})
