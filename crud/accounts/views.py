from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view,throttle_classes,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework.throttling import ScopedRateThrottle,AnonRateThrottle,UserRateThrottle
from .throttling import LoginRateThrottle
from rest_framework.exceptions import Throttled

# Registration View
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Registration successfull !"}, status=status.HTTP_201_CREATED)
    print(serializer.errors)    
    return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# Custom Exception Handler for Throttling
def custom_exception_handler(exc, context):
    if isinstance(exc, Throttled):  # Handle Throttle exception
        custom_response_data = {
            'error': 'Too many login attempts. Please try again after {} minutes.'.format((exc.wait // 60)+1)
        }
        return Response(custom_response_data, status=status.HTTP_429_TOO_MANY_REQUESTS)

    # If it's not a throttle exception, return the default response
    return None

# Login View with Throttle and Custom Exception Handling
@api_view(['POST'])
@throttle_classes([LoginRateThrottle])
def login(request):

    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        try:
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response({"error": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Login successful!',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# Logout View
@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logout successful!"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({"error": "Failed to log out. Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

