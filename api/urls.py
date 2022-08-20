from django.urls import path

from api import views

urlpatterns = [
    path('job-vacancy', views.JobVacancyListCreateAPI.as_view()),
    path('job-vacancy/<int:job_vacancy_id>', views.JobVacancyDetailUpdateDeleteAPI.as_view()),
]