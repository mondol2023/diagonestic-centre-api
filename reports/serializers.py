from rest_framework import serializers
from .models import ReportTemplate, TestReport, TestParameter

class TestParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestParameter
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class ReportTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportTemplate
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class TestReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestReport
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')