from django.forms import model_to_dict
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.templatetags.rest_framework import data
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterUserForm

from .models import Event, Ticket, Company
from rest_framework import viewsets
from .serializers import EventSerializer, TicketSerializer, CompanySerializer
# Create your views here.


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


# class SignUpView(CreateView):
#     template_name = 'register.html'
#     form_class = RegisterUserForm
#     success_url = reverse_lazy('register')
#
#
# class EventViewSet(viewsets.ModelViewSet):
#     queryset = Event.objects.all().order_by('title')
#     serializer_class = EventSerializer
#
#
# class TicketViewSet(viewsets.ModelViewSet):
#     queryset = Ticket.objects.all().order_by('number')
#     serializer_class = TicketSerializer
#
#
# class CompanyViewSet(viewsets.ModelViewSet):
#     queryset = Company.objects.all().order_by('title')
#     serializer_class = CompanySerializer


