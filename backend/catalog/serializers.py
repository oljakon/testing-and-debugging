from rest_framework import serializers
from django.contrib.auth.models import User
from .models import City, Industry, Company, JobVacancy, Application


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ('url', 'name')


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    industry = serializers.StringRelatedField(many=True)
    class Meta:
        model = Company
        fields = ('url', 'name', 'industry')


class IndustrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Industry
        fields = ('url', 'name')


class VacancySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = JobVacancy
        fields = ('url', 'title', 'company', 'industry', 'city', 'years_of_exp', 'type')


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    applicant = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Application
        fields = ('url', 'applicant', 'job', 'applied_on')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password')

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user