from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_user(request):
    # Your view logic here to create a user
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not (username or email) or not password:
        return Response({"error": "Both username/email and password are required"}, status=400)

    # Check if the user already exists
    if username and User.objects.filter(username=username).exists():
        return Response({"error": "User with this username already exists"}, status=400)

    if email and User.objects.filter(email=email).exists():
        return Response({"error": "User with this email already exists"}, status=400)

    # Create a new user
    user = User.objects.create_user(username=username, email=email, password=password)

    return Response({"message": "User created successfully"})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_user(request):
    # Your view logic here to authenticate and login a user using either username or email
    username_or_email = request.data.get('username_or_email')
    password = request.data.get('password')

    if not username_or_email or not password:
        return Response({"error": "Both username/email and password are required"}, status=400)

    # Try to authenticate with username
    user = authenticate(request, username=username_or_email, password=password)

    # If not successful, try to authenticate with email
    if not user:
        user
