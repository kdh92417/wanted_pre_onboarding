import json

from django.test import TestCase, Client

from api.models import (
    User,
    Company,
    JobVacancy
)


class JobVacancyListCreateAPITest(TestCase):
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

    def tearDown(self):
        Company.objects.all().delete()
        User.objects.all().delete()
        JobVacancy.objects.all().delete()
        
    def test_get_job_vacancy_list(self):
        client = Client()
        response = client.get(
            "/api/job-vacancy"
        )

        result = [
            {
                'id': 1,
                'company_name': '원티드',
                'company_country': '한국',
                'company_region': '서울',
                'position': '백엔드',
                'compensation': 100,
                'use_tech': 'Java'

            },
            {
                'id': 2,
                'company_name': '원티드',
                'company_country': '한국',
                'company_region': '서울',
                'position': '프론트',
                'compensation': 100,
                'use_tech': 'Javascript'
            },
            {
                'id': 3,
                'company_name': '원티드',
                'company_country': '한국',
                'company_region': '서울',
                'position': '머신러닝',
                'compensation': 100,
                'use_tech': 'Python'
            }
        ]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), result)
        
    def test_search_job_vacancy_list(self):
        client = Client()
        response = client.get(
            "/api/job-vacancy?search=python"
        )

        result = [
            {
                'id': 3,
                'company_name': '원티드',
                'company_country': '한국',
                'company_region': '서울',
                'position': '머신러닝',
                'compensation': 100,
                'use_tech': 'Python'
            }
        ]
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), result)
        
    def test_register_job_posting(self):
        client = Client()
        new_job_postring = {
            'company': 1,
            'position': '백엔드',
            'compensation': 100,
            'content': '네이버 백엔드 직군 채용합니다.',
            'use_tech': 'Java'
        }
        response = client.post(
            "/api/job-vacancy",
            json.dumps(new_job_postring),
            content_type="application/json"
        )
        
        self.assertEqual(response.status_code, 201)
    
    def test_register_job_posting_error(self):
        client = Client()
        new_job_posting = {
            'company': 2,
            'position': '백엔드',
            'compensation': 100,
            'content': '네이버 백엔드 직군 채용합니다.'
        }
        response = client.post(
            "/api/job-vacancy",
            json.dumps(new_job_posting),
            content_type="application/json"
        )
        error_message = response.json()
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(error_message['use_tech'][0], 'This field is required.')
        self.assertEqual(error_message['company'][0], 'Invalid pk "2" - object does not exist.')
