from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Appointment, AppointmentHistory
from .serializers import AppointmentSerializer
from accounts.models import User

# Create your views here.
class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'PATIENT':
            return Appointment.objects.filter(patient=user)
        elif user.user_type == 'DOCTOR':
            return Appointment.objects.filter(doctor=user)
        elif user.user_type in ['RECEPTIONIST', 'ADMIN']:
            return Appointment.objects.all()
        return Appointment.objects.none()
    
    @action(detail=True, methods=['post'])
    def confirm_appointment(self, request, pk=None):
        appointment = get_object_or_404(Appointment, pk=pk)
        
        if appointment.status != 'SCHEDULED':
            return Response(
                {'error': 'Only scheduled appointments can be confirmed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create history record
        AppointmentHistory.objects.create(
            appointment=appointment,
            status_changed_from=appointment.status,
            status_changed_to='CONFIRMED',
            changed_by=request.user,
            notes=request.data.get('notes', '')
        )
        
        appointment.status = 'CONFIRMED'
        appointment.save()
        
        return Response({'message': 'Appointment confirmed successfully'})
    
    @action(detail=False, methods=['get'])
    def today_appointments(self, request):
        today = timezone.now().date()
        appointments = self.get_queryset().filter(appointment_date=today)
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming_appointments(self, request):
        today = timezone.now().date()
        appointments = self.get_queryset().filter(
            appointment_date__gte=today,
            status__in=['SCHEDULED', 'CONFIRMED']
        ).order_by('appointment_date', 'appointment_time')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)