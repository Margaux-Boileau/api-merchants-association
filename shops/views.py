import uuid
from django.http import FileResponse
from forums.serializers import SimpleForumSerializer
from .serializers import ShopSerializer, UpdateShopSerializer
from django.db.models import Q
from .models import Shop
from accounts.models import Account
from forums.models import Forum
from media.models import Media
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import base64

# /shops/
class ShopListView(APIView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.permission_classes = []
        else:
            self.permission_classes = []

        return super().dispatch(request, *args, **kwargs)
    
    # PERMISIONS: all
    def get(self, request):
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)
    
    # PERMISSIONS: admin
    def post(self, request):
        data = request.data
        media = data.get('image', None)  
        
        if media:
            decoded = base64.b64decode(media)

            media_name = f'uploads/{uuid.uuid4()}.jpg'

            with open(media_name, 'wb') as f:
                f.write(decoded)
            
            media_obj = Media.objects.create(id=media_name)

            data['image'] = media_name

        serializer = ShopSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# /shops/<pk>/
class ShopDetailView(APIView):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'PUT':
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []

        return super().dispatch(request, *args, **kwargs)
    
    # PERMISIONS: all
    def get(self, request, pk):
        try:
            shop = Shop.objects.get(pk=pk)
        except Shop.DoesNotExist:
            return Response({"error": "Shop does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ShopSerializer(shop)
        print(serializer.data["image"])

        return Response(serializer.data)
    
    # PERMISIONS: owner shop
    def put(self, request, pk):
        try:
            shop = Shop.objects.get(pk=pk)
        except Shop.DoesNotExist:
            return Response({"error": "Shop not found"}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        print(request.data)
        if user in shop.workers.all() and user.is_owner_of_shop:
            
            serializer = UpdateShopSerializer(shop, data=request.data, partial=True)
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                updated_shop = Shop.objects.get(pk=pk)
                full_shop_serializer = ShopSerializer(updated_shop)
                return Response(full_shop_serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You do not have permission to update this shop."}, status=status.HTTP_403_FORBIDDEN)

# /shops/<pk>/employees/
# PERMISIONS: owner shop
class ShopEmployeesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            shop = Shop.objects.get(pk=pk)
        except Shop.DoesNotExist:
            return Response({"error": "Shop not found."}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        
        if user in shop.workers.all() or user.is_owner_of_shop:
            worker_names = [worker.username for worker in shop.workers.all()]
            return Response(worker_names, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You do not have permission to access this resource."}, status=status.HTTP_403_FORBIDDEN)
    
    def post(self, request, pk):
        try:
            shop = Shop.objects.get(pk=pk)
        except Shop.DoesNotExist:
            return Response({"error": "Shop not found."}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        
        if user.is_owner_of_shop:
            new_worker_name = request.data.get('worker')
            
            try:
                new_worker = Account.objects.get(username=new_worker_name)
            except Account.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            shop.workers.add(new_worker)
            shop.save()
            worker_names = [worker.username for worker in shop.workers.all()]
            return Response(worker_names, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You do not have permission to modify workers in this shop."}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, pk):
        try:
            shop = Shop.objects.get(pk=pk)
        except Shop.DoesNotExist:
            return Response({"error": "Shop not found."}, status=status.HTTP_404_NOT_FOUND)
        
        user = request.user
        
        if user.is_owner_of_shop:
            worker_name = request.data.get('worker')
            
            try:
                worker = shop.workers.get(username=worker_name)
            except Account.DoesNotExist:
                return Response({"error": "Worker not found in this shop."}, status=status.HTTP_404_NOT_FOUND)
            
            shop.workers.remove(worker)
            shop.save()
            
            return Response({"message": "Worker successfully removed from the shop."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You do not have permission to modify workers in this shop."}, status=status.HTTP_403_FORBIDDEN)

# /shops/<pk>/forums/
# PERMISIONS: employees shop
@api_view(['GET'])
def get_shop_forums_view(request, pk):
    try:
        shop = Shop.objects.get(pk=pk)
    except Shop.DoesNotExist:
        return Response({"error": "Shop not found."}, status=status.HTTP_404_NOT_FOUND)
    
    forums = Forum.objects.filter(read_members=shop)
    serializers = SimpleForumSerializer(forums, many=True)
    return Response(serializers.data, status=status.HTTP_200_OK)

# /shops/<pk>/image/
# PERMISIONS: all
@api_view(['GET'])
def get_shop_image_view(request, pk):
    try:
        shop = Shop.objects.get(pk=pk)
    except Shop.DoesNotExist:
        return Response({"error": "Shop not found."}, status=status.HTTP_404_NOT_FOUND)

    media = shop.image.id
    img = open('uploads/' + media, 'rb')

    response = FileResponse(img)

    return response