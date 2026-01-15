from django.shortcuts import get_object_or_404
from .serializers import (
    RegisterUserSerializer,
    LoginSerializer,
)
from rest_framework import generics, permissions, status, filters,viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User,Group
from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='manager').exists()
        )

class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.groups.filter(name='delivery crew').exists()
        )
    
            

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "user": RegisterUserSerializer(user).data,
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {
                "user": RegisterUserSerializer(user).data,
                "token": token.key,
            },
            status=status.HTTP_200_OK,
        )

@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data.get('username')

    if not username:
        return Response(
            {'message': 'username is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = get_object_or_404(User, username=username)
    managers, created = Group.objects.get_or_create(name='manager')

    if request.method == 'POST':
        managers.user_set.add(user)
        return Response(
            {'message': f'{username} authenticated and added to manager group'},
            status=status.HTTP_200_OK
        )

    if request.method == 'DELETE':
        managers.user_set.remove(user)
        return Response(
            {'message': f'{username} removed from the manager group'},
            status=status.HTTP_200_OK
        )
        

@api_view(['GET','DELETE'])
@permission_classes([IsAdminUser])
def list_managers(request,pk=None):
    try:
        manager_group=Group.objects.get(name='manager')
    except Group.DoesNotExist():
        return Response({'managers':[]})
    
    if pk:
        user = get_object_or_404(manager_group.user_set.add, pk=pk)
        data = {'id': user.id, 'username': user.username, 'email': user.email}
        return Response({'manager':data})
    
    else:
        users=manager_group.user_set.all()
        data = [ {'id': user.id, 'username': user.username, 'email': user.email}
        for user in users]
        
        return Response({'managers':data})
    
    
    
@api_view(['POST'])
@permission_classes([IsManager])
def delivery_crew(request):
    username = request.data.get('username')

    if not username:
        return Response(
            {'message': 'username is required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = get_object_or_404(User, username=username)
    delivery_crew, created = Group.objects.get_or_create(name='delivery crew')

    if request.method == 'POST':
        delivery_crew.user_set.add(user)
        return Response(
            {'message': f'{username} authenticated and added to delivery crew group'},
            status=status.HTTP_200_OK
        )

    if request.method == 'DELETE':
        delivery_crew.user_set.remove(user)
        return Response(
            {'message': f'{username} removed from the delivery crew group'},
            status=status.HTTP_200_OK
        )

@api_view(['GET','DELETE'])
@permission_classes([IsManager])

def list_delivery_crew(request,pk=None):
    try:
        delivery_crew_group=Group.objects.get(name='delivery crew')
    except Group.DoesNotExist():
        return Response({'delivery crew':[]})
    
    if pk:
        user = get_object_or_404(delivery_crew_group.user_set.add, pk=pk)
        data={'id':user.id, 'username':user.username,'email':user.email}
        
        return Response({'delivery crew':data})
    else:
        users=delivery_crew_group.user_set.all()
        
        data=[{
            'id':u.id,
            'username':u.username,
            'email':u.email
        }
              for u in users]
        return Response({'delivery crew':data})
