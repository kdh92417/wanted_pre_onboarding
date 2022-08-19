from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    region = models.CharField(max_length=20)

    class Meta:
        db_table = 'companies'


class JobVacancy(models.Model):
    position = models.CharField(max_length=50)
    compensation = models.IntegerField()
    content = models.CharField(max_length=3000)
    use_tech = models.CharField(max_length=100)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'job_vacancies'


# class Tech(models.Model):
#     name = models.CharField(max_length=20)
#
#     class Meta:
#         db_table = 'tech'
#
#
# class UseTech(models.Model):
#     tech_id = models.ForeignKey(Tech, on_delete=models.CASCADE)
#     job_vacancy_id = models.ForeignKey(JobVacancy, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'use_tech'


class User(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'


class Applications(models.Model):
    job_vacancy_id = models.ForeignKey(JobVacancy, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'applications'
