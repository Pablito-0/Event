
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterUserForm

from .models import Event, Ticket, Company
from rest_framework import viewsets, status, generics
from .serializers import EventSerializer, TicketSerializer, CompanySerializer


def get_event(request, pk: int):
    event = Event.objects.get(id=pk)
    return JsonResponse({
        "id": event.id,
        "title": event.title,
        "count": event.ticket_count,
        "org": {
            "id": event.organisator_id,
            "title": event.organisator.title,
            "created": event.organisator.created_at,
        }
    })


def get_all_events(request):
    events = Event.objects.all()
    return JsonResponse({
        "code": 200,
        "data": [
            {
                "id": e.id,
                "title": e.title,
                "count": e.ticket_count,
                "organisator_id": e.organisator_id,
            } for e in events]
    })


@api_view(["POST", "GET"])
def showall(request):
    serializer = TicketSerializer(Ticket.objects.all(), many=True)
    return Response(serializer.data)


@api_view(["POST", "GET"])
def showone(request, pk: int):
    serializer = TicketSerializer(Ticket.objects.get(pk=pk), many=True)
    return Response(serializer.data)


@csrf_exempt
@api_view(["POST", "GET"])
def test_drf(request):
    if request.method == 'GET':
        snippets = Event.objects.all()
        serializer = EventSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@api_view(["DELETE"])
def deleted(request, pk: int):
    event = Event.objects.get(pk=pk)
    event.delete()
    return Response(status=204)


@api_view(["GET"])
def showstatus(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)


class EventGet(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class TicketGet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CompanyGet(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser]


