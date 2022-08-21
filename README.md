# 원티드 백엔드 과제

HTTP Method GET, POST, PUT, DELETE에 의한 Restful API를 설계하고 Django Rest framework를 이용하여 요구사항 구현

- `GET`: 리스트조회 및 상세조회
- `POST`: 채용공고 지원 및 생성
- `PUT` : 채용공고 수정
- `DELETE` : 채용공고 삭제

## API 개요

- `api/job-vacancy`
  - GET Method: 검색기능이있는 채용공고리스트 조회
  - POST Method: 채용공고 등록

- `api/job-vacancy/application_id`
  - GET Method: 채용공고 상세 조회
  - POST Method: 채용공고 상세 수정
  - DELETE Method: 채용공고 상세 삭제

- `api/application`
  - POST Method: 채용공고에 지원
