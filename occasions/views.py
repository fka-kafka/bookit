from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# drf_yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Occasion
from .serializers import OccasionSerializer


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('location', openapi.IN_QUERY,
                          description="Filter by location", type=openapi.TYPE_STRING),
        openapi.Parameter('date', openapi.IN_QUERY,
                          description="Filter by date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        openapi.Parameter('keyword', openapi.IN_QUERY,
                          description="Search keyword", type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY,
                          description="Page number", type=openapi.TYPE_INTEGER),
    ],
    responses={200: openapi.Response('List', OccasionSerializer(many=True))}
)
@swagger_auto_schema(
    method='post',
    request_body=OccasionSerializer,
    responses={201: openapi.Response(
        'Created', OccasionSerializer), 400: 'Bad Request'}
)
@api_view(['GET', 'POST'])
def occasion_list(request):
    if request.method == 'GET':
        # Filtering
        occasions = Occasion.objects.all()
        print(occasions)

        location = request.query_params.get('location')
        if location:
            occasions = occasions.filter(location__icontains=location)

        date = request.query_params.get('date')
        if date:
            occasions = occasions.filter(date_time__date=date)

        keyword = request.query_params.get('keyword')
        if keyword:
            occasions = occasions.filter(
                Q(occasion_name__icontains=keyword) | Q(location__icontains=keyword))

        # Pagination
        page = request.query_params.get('page', 1)
        paginator = Paginator(occasions, 10)
        occasions_page = paginator.get_page(page)

        serializer = OccasionSerializer(occasions_page, many=True)
        return Response({
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': int(page),
            'results': serializer.data
        })

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_organizer:
            return Response({'error': 'Only organizers can create occasions'}, status=status.HTTP_403_FORBIDDEN)

        serializer = OccasionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('occasion_id', openapi.IN_PATH,
                          description="Occasion UUID", type=openapi.TYPE_STRING, format='uuid')
    ],
    responses={200: openapi.Response(
        'OK', OccasionSerializer), 404: 'Not Found'}
)
@swagger_auto_schema(
    method='put',
    request_body=OccasionSerializer,
    manual_parameters=[
        openapi.Parameter('occasion_id', openapi.IN_PATH,
                          description="Occasion UUID", type=openapi.TYPE_STRING, format='uuid')
    ],
    responses={200: openapi.Response(
        'OK', OccasionSerializer), 400: 'Bad Request', 404: 'Not Found'}
)
@swagger_auto_schema(
    method='delete',
    manual_parameters=[
        openapi.Parameter('occasion_id', openapi.IN_PATH,
                          description="Occasion UUID", type=openapi.TYPE_STRING, format='uuid')
    ],
    responses={204: 'No Content', 403: 'Forbidden', 404: 'Not Found'}
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def occasion_detail(request, occasion_id):
    """Retrieve, update or delete an occasion"""

    try:
        occasion = Occasion.objects.get(occasion_id=occasion_id)
    except Occasion.DoesNotExist:
        return Response({'error': 'Occasion not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OccasionSerializer(occasion)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if occasion.organizer != request.user:
            return Response({'error': 'You can only update your own occasions'}, status=status.HTTP_403_FORBIDDEN)

        serializer = OccasionSerializer(
            occasion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if occasion.organizer != request.user:
            return Response({'error': 'You can only delete your own occasions'}, status=status.HTTP_403_FORBIDDEN)

        occasion.delete()
        return Response({'message': 'Occasion deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
