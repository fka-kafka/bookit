from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from occasions.models import Occasion
from .models import Reservation

# Create your views here.


# View for creating reservation
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_reservation(request, occasion_id):
    attendee = request.user
    try:
        occasion = Occasion.objects.get(occasion_id=occasion_id)
    except Occasion.DoesNotExist:
        return Response({
            'message': 'Occasion does not exist'
        }, status=status.HTTP_404_NOT_FOUND)

    if request.user.is_organizer:
        return Response({
            'message': 'Only attendees can RSVP Events'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    reservation, created = Reservation.objects.get_or_create(
        attendee=attendee,
        occasion=occasion,
    )

    if not created:
        return Response({"error": "You have already RSVP'd to this event."},
                        status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "RSVP submitted and pending approval."},
                    status=status.HTTP_201_CREATED)


# View for approving reservations

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_reservations(request):
    """ Get all reservations """
    return Response({
        'results': []}
    )
