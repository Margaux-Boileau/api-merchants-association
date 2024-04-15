from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from shops.models import Shop
from shops.serializers import ShopSerializer
from .models import Account
from .serializers import AccountSerializer, RegisterSerializer


@api_view(['POST', ])
def register_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': AccountSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def login_view(request):
    if request.method == 'POST':     
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:            
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': AccountSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', ])
@permission_classes([IsAuthenticated, ])
def account_detail_view(request, username):
    user = request.user
    if str(user.username) == username:
        try:
            account = Account.objects.get(username=username)
            shop = account.shop_set.first()
            serializer = AccountSerializer(account)
            shop_data = ShopSerializer(shop).data if shop else None
            response_data = {
                'user': serializer.data,
                'shop': shop_data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def account_change_password_view(request, username):
    user = request.user
    if user.username == username:
        new_password = request.data.get('password')
        if new_password:
            # Set the new password for the user
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "New password is required."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "You do not have permission to change the password for this user."}, status=status.HTTP_403_FORBIDDEN)