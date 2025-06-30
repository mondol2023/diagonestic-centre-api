from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import User, Patient, Doctor, LabTechnician, Receptionist
from .serializers import (
    UserSerializer, UserRegistrationSerializer, LoginSerializer,
    PatientSerializer, DoctorSerializer, 
    LabTechnicianSerializer, ReceptionistSerializer
)

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type in ['ADMIN', 'RECEPTIONIST']:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def doctors(self, request):
        doctors = User.objects.filter(user_type='DOCTOR', is_active=True)
        serializer = self.get_serializer(doctors, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def patients(self, request):
        if request.user.user_type not in ['ADMIN', 'RECEPTIONIST']:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        
        patients = User.objects.filter(user_type='PATIENT', is_active=True)
        serializer = self.get_serializer(patients, many=True)
        return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'User registered successfully'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'user': UserSerializer(user).data,
                    'token': token.key,
                    'message': 'Login successful'
                })
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'PATIENT':
            return Patient.objects.filter(user=user)
        elif user.user_type in ['ADMIN', 'RECEPTIONIST', 'DOCTOR']:
            return Patient.objects.all()
        return Patient.objects.none()

class DoctorViewSet(viewsets.ModelViewSet):
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'DOCTOR':
            return Doctor.objects.filter(user=user)
        elif user.user_type in ['ADMIN', 'RECEPTIONIST']:
            return Doctor.objects.all()
        return Doctor.objects.filter(user__is_active=True)
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        profile = get_object_or_404(Doctor, pk=pk)
        return Response({
            'available_days': profile.available_days.split(','),
            'available_time_start': profile.available_time_start,
            'available_time_end': profile.available_time_end,
            'consultation_fee': profile.consultation_fee
        })

class LabTechnicianViewSet(viewsets.ModelViewSet):
    serializer_class = LabTechnicianSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'LAB_TECHNICIAN':
            return LabTechnician.objects.filter(user=user)
        elif user.user_type in ['ADMIN', 'RECEPTIONIST']:
            return LabTechnician.objects.all()
        return LabTechnician.objects.filter(user__is_active=True)


class ReceptionistViewSet(viewsets.ModelViewSet):
    serializer_class = ReceptionistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'RECEPTIONIST':
            return Receptionist.objects.filter(user=user)
        elif user.user_type == 'ADMIN':
            return Receptionist.objects.all()
        return Receptionist.objects.filter(user__is_active=True)

