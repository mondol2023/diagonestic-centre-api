from rest_framework import serializers
from .models import User, Patient ,Doctor , LabTechnician, Receptionist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['all']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['all']

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['all']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['all']

class LabTechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTechnician
        fields = ['all']

class ReceptionistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receptionist
        fields = ['all']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return {'user': user}
