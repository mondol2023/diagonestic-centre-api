from django.urls import path
from . import views

urlpatterns = [
    path(
        'appointments/',
        views.AppointmentViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='appointment-list'
    ),
    path(
        'appointments/<int:pk>/',
        views.AppointmentViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='appointment-detail'
    ),
    path(
        'appointments/<int:pk>/confirm_appointment/',
        views.AppointmentViewSet.as_view({'post': 'confirm_appointment'}),
        name='appointment-confirm'
    ),
    path(
        'appointments/today_appointments/',
        views.AppointmentViewSet.as_view({'get': 'today_appointments'}),
        name='appointment-today'
    ),
    path(
        'appointments/upcoming_appointments/',
        views.AppointmentViewSet.as_view({'get': 'upcoming_appointments'}),
        name='appointment-upcoming'
    ),
]