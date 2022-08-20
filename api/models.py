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
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        db_table = 'job_vacancies'


class User(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'users'


class Applications(models.Model):
    job_vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'applications'
