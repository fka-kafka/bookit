from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# drf_yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from occasions.models import Occasion
from authentication.models import User
from .models import Reservation

# View for creating reservation


@swagger_auto_schema(
    methods=['post'],
    manual_parameters=[
        openapi.Parameter('occasion_id', openapi.IN_PATH,
                          description="Occasion UUID", type=openapi.TYPE_STRING, format='uuid')
    ],
    responses={201: 'RSVP submitted', 404: 'Not Found', 400: 'Bad Request'}
)
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

@swagger_auto_schema(
    methods=['put'],
    manual_parameters=[
        openapi.Parameter('reservation_id', openapi.IN_PATH,
                          description="Reservation UUID", type=openapi.TYPE_STRING, format='uuid')
    ],
    responses={200: 'Status changed', 404: 'Not Found', 406: 'Not Acceptable'}
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def approve_reservation(request, reservation_id):
    user: User = request.user
    if user.is_attendee:
        return Response({
            'message': 'Only organizers can approve RSVPs.'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        reservation = Reservation.objects.get(reservation_id=reservation_id)
        reservation.approved = True
        reservation.save()
        return Response({
            "message": "status changed",
            "details": f"{reservation.approved}",
        })
    except Exception as exception:
        return Response(
            {
                'message': f'An error occured: {exception}'
            }
        )
