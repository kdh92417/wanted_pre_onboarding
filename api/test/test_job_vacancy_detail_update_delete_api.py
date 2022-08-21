import json

from django.test import TestCase, Client

from api.models import (
    User,
    Company,
    JobVacancy
)


class JobVacancyDetailUpdateDeleteAPITest(TestCase):
    def setUp(self):
        User.objects.create(
            name='adam'
        )
        wanted = Company(
            name='원티드',
            country='한국',
            region='서울'
        )
        naver = Company(
            name='네이버',
            country='한국',
            region='판교'
        )
        wanted.save()
        naver.save()
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

    def test_update_job_posting(self):
        client = Client()
        update_job_postring = {
            'position': '백엔드',
            'compensation': 100,
            'content': '백엔드 채용합니다.',
            'use_tech': 'Go', # Java -> Go로 변경
            'company': 2
        }

        response = client.put(
            "/api/job-vacancy/1",
            json.dumps(update_job_postring),
            content_type="application/json"
        )

        updated_job_vacancy_object = JobVacancy.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_job_vacancy_object.use_tech, 'Go')
        self.assertEqual(updated_job_vacancy_object.company.id, 1) # 회사는 변경 안됨
        
    def test_update_job_posting_error(self):
        client = Client()
        update_job_postring = {
            'position': '백엔드',
            'use_tech': 'Go', # Java -> Go로 변경
            'company': 2,
        }

        response = client.put(
            "/api/job-vacancy/4",
            json.dumps(update_job_postring),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'JobVacancy matching query does not exist.')

    def test_delete_job_vacancy(self):
        client = Client()
        response = client.delete(
            "/api/job-vacancy/3",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(JobVacancy.objects.filter(id=3).first(), None)
        
    def test_delete_job_vacancy_error(self):
        client = Client()
        response = client.delete(
            "/api/job-vacancy/5",
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'JobVacancy matching query does not exist.')
    
    def test_get_job_posting_detail(self):
        client = Client()
        response = client.get(
            "/api/job-vacancy/3",
        )
        
        data = {
            'id': 3,
            'company_name': '원티드',
            'company_country': '한국',
            'company_region': '서울',
            'position': '머신러닝',
            'compensation': 100,
            'content': '머신러닝 채용합니다.',
            'use_tech': 'Python',
            'other_job_vacancy': [1, 2]
        }

        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result, data)
        self.assertEqual(result['other_job_vacancy'], data['other_job_vacancy'])
        
    def test_get_job_posting_detail_error(self):
        client = Client()
        response = client.get(
            "/api/job-vacancy/5",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'JobVacancy matching query does not exist.')
