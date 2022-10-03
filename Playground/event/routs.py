from django.urls import path

from event.views import get_all_events, get_event, test_drf, deleted, showall, showone

urlpatterns = [
    path('', get_all_events),
    path('event/<int:pk>/', get_event),
    path('drf/', test_drf),
    path('del/<int:pk>', deleted),
    path('showone/<int:pk>', showone),
    path('showall/', showall),
    ]
