from django.db.models import Q

from rest_framework import serializers

from api.models import JobVacancy


class JobVacancyCreateUpdateListSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_country = serializers.CharField(source='company.country', read_only=True)
    company_region = serializers.CharField(source='company.region', read_only=True)

    class Meta:
        model = JobVacancy
        fields = '__all__'
        extra_kwargs = {
            'content': {'write_only': True},
            'company': {'write_only': True}
        }


class JobVacancyDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)
    company_country = serializers.CharField(source='company.country', read_only=True)
    company_region = serializers.CharField(source='company.region', read_only=True)
    other_job_vacancy = serializers.SerializerMethodField(method_name='get_other_job_vacancy')

    def get_other_job_vacancy(self, obj):
        return [job.id for job in JobVacancy.objects.filter(
            Q(company=obj.company.id) & ~Q(id=obj.id)
        )]

    class Meta:
        model = JobVacancy
        exclude = ['company']