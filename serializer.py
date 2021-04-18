from rest_framework import serializers
from .models import Student, City

class StudentSerializer(serializers.ModelSerializer):
    #city_name = serializers.StringRelatedField(many=True)
    class Meta:
        model = Student
        fields = ['id','name','rollno','cityName']
        lookup_field = ['id']

class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ['id','city_name', 'state']
        lookup_field = ['id']
