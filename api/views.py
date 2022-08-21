from django.db.models import Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Applications, JobVacancy
from api.serializers import (
    ApplicationSerializer,
    JobVacancyCreateUpdateListSerializer,
    JobVacancyDetailSerializer
)


class JobVacancyListCreateAPI(APIView):
    def get(self, request):
        queryset = JobVacancy.objects.select_related('company')
        search = request.query_params.get('search', None)
        if search:
            queryset = JobVacancy.objects.select_related('company').filter(
                Q(company__name__icontains=search)
                | Q(use_tech__icontains=search)
                | Q(position__icontains=search)
            )

        serializer = JobVacancyCreateUpdateListSerializer(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = JobVacancyCreateUpdateListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobVacancyDetailUpdateDeleteAPI(APIView):
    def delete(self, request, job_vacancy_id):
        try:
            job_vacancy_object = JobVacancy.objects.get(id=job_vacancy_id)
            job_vacancy_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Applications.DoesNotExist as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, job_vacancy_id):
        try:
            if 'company' in request.data:
                del request.data['company']

            job_vacancy_object = JobVacancy.objects.get(id=job_vacancy_id)
            update_job_vacancy_serializer = JobVacancyCreateUpdateListSerializer(
                job_vacancy_object, data=request.data, partial=True
            )

            if update_job_vacancy_serializer.is_valid(raise_exception=True):
                update_job_vacancy_serializer.save()
                return Response(data=update_job_vacancy_serializer.data, status=status.HTTP_200_OK)

        except Applications.DoesNotExist as e:
            return Response(data=str(e), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, job_vacancy_id):
        queryset = JobVacancy.objects.select_related('company').get(id=job_vacancy_id)
        serializer = JobVacancyDetailSerializer(queryset)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ApplicationAPI(APIView):

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    