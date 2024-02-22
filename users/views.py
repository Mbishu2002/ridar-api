from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not (username or email) or not password:
        return Response({"error": "Both username/email and password are required"}, status=400)

    if username and User.objects.filter(username=username).exists():
        return Response({"error": "User with this username already exists"}, status=400)

    if email and User.objects.filter(email=email).exists():
        return Response({"error": "User with this email already exists"}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)

    # Token generation
    token, created = Token.objects.get_or_create(user=user)

    # Email verification using django-allauth
    email_confirmation = EmailConfirmation.create(user)
    email_confirmation.sent = True
    email_confirmation.save()
    email_confirmation.sent_at = email_confirmation.sent_at or timezone.now()
    email_confirmation.save()
    email_confirmation.confirm()

    return Response({"message": "User created successfully. Verification email sent."})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def login_user(request):
    username_or_email = request.data.get('username_or_email')
    password = request.data.get('password')

    if not username_or_email or not password:
        return Response({"error": "Both username/email and password are required"}, status=400)

    user = authenticate(request, username=username_or_email, password=password)

    if not user:
        return Response({"error": "Invalid credentials"}, status=401)

    login(request, user)

    token, created = Token.objects.get_or_create(user=user)

    return Response({"message": "Login successful", "token": token.key})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def forgot_password(request):
    email = request.data.get('email')

    if not email:
        return Response({"error": "Email is required to reset the password"}, status=400)

    user = get_object_or_404(User, email=email)

    # Generate a password reset token using django-allauth
    email_confirmation = EmailConfirmation.create(user)
    email_confirmation.sent = True
    email_confirmation.save()
    email_confirmation.sent_at = email_confirmation.sent_at or timezone.now()
    email_confirmation.save()
    email_confirmation.confirm()  

    # Send an email with the password reset link
    reset_link = f"http://localhost:3000/reset-password/{email_confirmation.key}/"
    send_mail(
        'Reset Your Password',
        f'Click the following link to reset your password: {reset_link}',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )

    return Response({"message": "Password reset email sent."})

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def reset_password(request):
    reset_key = request.data.get('reset_key')
    new_password = request.data.get('new_password')

    if not reset_key or not new_password:
        return Response({"error": "Both reset_key and new_password are required"}, status=400)

    try:
        email_confirmation = EmailConfirmation.objects.get(key=reset_key, sent=True)
        user = email_confirmation.email_address.user
    except EmailConfirmation.DoesNotExist:
        return Response({"error": "Invalid or expired reset key"}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"message": "Password reset successful."})