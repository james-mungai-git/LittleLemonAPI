from django.shortcuts import get_object_or_404
from .serializers import MenuItemSerializer
from LittleLemon.models import MenuItem
from rest_framework import status, filters,viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage
from accounts.views import IsManager
    
            
class Pagination:
    page_size = 10
    page_size_query_param = 'perpage'
    max_page_size = 50



@api_view(['GET', 'POST'])
def menuitems(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()

        category_name = request.query_params.get('category')
        price = request.query_params.get('price')
        ordering = request.query_params.get('ordering')
        search = request.query_params.get('search')
        perpage = int(request.query_params.get('perpage', 10))
        page = int(request.query_params.get('page', 1))

        if category_name:
            items = items.filter(category__title=category_name)

        if price:
            items = items.filter(price__lte=price)

        if search:
            items = items.filter(title__icontains=search)

        if ordering:
            items = items.order_by(*ordering.split(','))

        paginator = Paginator(items, perpage)

        try:
            items = paginator.page(page)
        except EmptyPage:
            items = []

        serializer = MenuItemSerializer(items, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if not (request.user.is_staff or request.user.groups.filter(name='manager').exists()):
            return Response(
                {"detail": "Not authorized"},
                status=status.HTTP_403_FORBIDDEN
            )


        serializer = MenuItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def singleitem(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    serializer = MenuItemSerializer(item)
    return Response(serializer.data)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['price', 'inventory']
    search_fields = ['title', 'category__title']

    def get_permissions(self):
        if self.request.method in ['POST','PUT','PATCH','DELETE']:
            return [IsManager()]
        return super().get_permissions()
