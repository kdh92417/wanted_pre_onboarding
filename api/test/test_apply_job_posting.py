import json

from django.test import TestCase, Client

from api.models import (
    User,
    Company,
    JobVacancy,
    Applications
)


class ApplicationAPIAPITest(TestCase):
    def setUp(self):
        User.objects.create(
            name='adam'
        )
        wanted = Company(
            name='원티드',
            country='한국',
            region='서울'
        )
        wanted.save()
        JobVacancy.objects.bulk_create([
            JobVacancy(
                position='백엔드',
                compensation='100',
                content='백엔드 채용합니다.',
                use_tech='Java',
                company=wanted
            ),
            JobVacancy(
                position='프론트',
                compensation='100',
                content='프론트 채용합니다.',
                use_tech='Javascript',
                company=wanted
            ),
            JobVacancy(
                position='머신러닝',
                compensation='100',
                content='머신러닝 채용합니다.',
                use_tech='Python',
                company=wanted
            )
        ])
        Applications.objects.create(
            job_vacancy=JobVacancy.objects.get(id=1),
            user=User.objects.get(id=1)
        )

    def tearDown(self):
        User.objects.all().delete()
        Applications.objects.all().delete()
        Company.objects.all().delete()
        JobVacancy.objects.all().delete()

    def test_apply_job_posting(self):
        client = Client()
        new_application = {
            "job_vacancy": 2,
            "user": 1
        }

        response = client.post(
            "/api/application",
            json.dumps(new_application),
            content_type="application/json"
        )
        
        data = {'id': 2, 'job_vacancy': 2, 'user': 1}

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data)
        
    def test_apply_same_job_posting_error(self):
        client = Client()
        new_application = {
            "job_vacancy": 1,
            "user": 1
        }

        response = client.post(
            "/api/application",
            json.dumps(new_application),
            content_type="application/json"
        )

        error_message = 'The fields job_vacancy, user must make a unique set.'

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['non_field_errors'][0], error_message)
        
    def test_apply_job_posting_error(self):
        client = Client()
        new_application = {
            "job_vacancy": 5,
            "user": 3
        }

        response = client.post(
            "/api/application",
            json.dumps(new_application),
            content_type="application/json"
        )
        
        does_not_exist_user_pk_3 = 'Invalid pk "3" - object does not exist.'
        does_not_exist_job_vacancy_pk_5 = 'Invalid pk "5" - object does not exist.'

        result = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(result['job_vacancy'][0], does_not_exist_job_vacancy_pk_5)
        self.assertEqual(result['user'][0], does_not_exist_user_pk_3)
