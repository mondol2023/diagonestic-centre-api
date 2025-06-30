from rest_framework import serializers
from .models import TestCategory, Test, TestPackage

class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class TestSerializer(serializers.ModelSerializer):
    category = TestCategorySerializer(read_only=True)

    class Meta:
        model = Test
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class TestPackageSerializer(serializers.ModelSerializer):
    tests = TestSerializer(many=True, read_only=True)

    class Meta:
        model = TestPackage
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')