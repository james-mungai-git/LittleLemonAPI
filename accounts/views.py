from django.shortcuts import get_object_or_404, render,redirect
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
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

        
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

        return render(request,'accounts/login.html')
        


@api_view(['POST'])
@permission_classes([IsAdminUser])
def groups(request):
   username= request.data.get('username')
   group_name=request.data.get('group name')
   
   if not username or not group_name:
       return Response({'message':'username and group_name are required'},status.HTTP_400_BAD_REQUEST)
   
   user=get_object_or_404(User, username=username)
   group,created =Group.objects.get_or_create(name=group_name)
   
   if group_name.lower() == 'manager' and not request.user.is_staff:
       return Response({'message':'only admins can add/remove users from manager group'})
   
   if request.method == 'POST':
       group.user_set.add(user)
       return Response({'message':f'{username} has been added to {group_name} group'},status.HTTP_200_OK)
   
   elif request.method == 'DELETE':
       group.user_set.remove(user)
       return Response({'message':f'{username} has been removed from {group_name} group'},status.HTTP_200_OK)
   
   else:
       return Response({'message':'both user name and group name are required'})   
   
   
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
