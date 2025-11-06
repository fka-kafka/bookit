from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Occasion
from .serializers import OccasionSerializer


@api_view(['GET', 'POST'])
def occasion_list(request):
    if request.method == 'GET':
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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
