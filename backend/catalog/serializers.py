from rest_framework import serializers

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