import json
from datetime import datetime
from django.urls import reverse
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework.test import APITestCase

from study.models import User, Tutor, Student, StudyGroup, Subject, Course, Role, Gender, Report, ReportType, Status
from study.selializers import UserSerializer, TutorReadSerializer, SubjectSerializer,\
                            CourseSerializer, StudyGroupSerializer, StudentReadSerializer, ReportSerializer


class UsersApiTestCase(APITestCase):
    def setUp(self):
        self.user_owner = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Petrov', role=Role.ADMIN)
        self.user_not_owner = User.objects.create(username='user2', password='user2', first_name='Ivan', last_name='Sidorov', role=Role.ADMIN)

    def test_get_list(self):
        url = reverse('user-list')
        response = self.client.get(url)
        serializer_data = UserSerializer([self.user_owner, self.user_not_owner], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_item(self):
        url = reverse('user-detail', args=(self.user_owner.id,))
        response = self.client.get(url)

        serializer_data = UserSerializer(self.user_owner).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(2, User.objects.all().count())
        url = reverse('user-list')
        data = {
            'id': 3,
            'first_name': 'Ivan',
            'last_name': 'Ivanov'
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, User.objects.all().count())

    def test_update(self):
        url = reverse('user-detail', args=(self.user_owner.id,))
        data = {
            'id': self.user_owner.id,
            'first_name': 'Petr',
            'last_name': 'Petrov'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_owner)
        response = self.client.put(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.user_owner.refresh_from_db()
        self.assertEqual('Petr', self.user_owner.first_name)

    def test_delete(self):
        self.assertEqual(2, User.objects.all().count())

        url = reverse('user-detail', args=(self.user_owner.id,))
        self.client.force_login(self.user_owner)
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, User.objects.all().count())

    def test_permissions(self):
        data = {
            'id': self.user_owner.id,
            'first_name': 'Ivan',
            'last_name': 'Petrov'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_not_owner)

        methods_list = ['put', 'delete']
        for method in methods_list:
            if method == 'put':
                url = url = reverse('user-detail', args=(self.user_owner.id,))
                response = self.client.put(url, data=json_data, content_type='application/json')
            if method == 'delete':
                url = url = reverse('user-detail', args=(self.user_owner.id,))
                response = self.client.delete(url)
            self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class TutorApiTestCase(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Sidorov', role=Role.ADMIN)
        self.user_tutor = User.objects.create(username='user2', password='user2', first_name='Ivan', last_name='Petrov', role=Role.TUTOR)

    def test_get_list(self):
        tutor = Tutor.objects.create(user_id=self.user_tutor.id)

        url = reverse('tutor-list')
        response = self.client.get(url)

        serializer_data = TutorReadSerializer([tutor], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_item(self):
        tutor = Tutor.objects.create(user_id=self.user_tutor.id)

        url = reverse('tutor-detail', args=(tutor.id,))
        response = self.client.get(url)

        serializer_data = TutorReadSerializer(tutor).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(0, Tutor.objects.all().count())
        url = reverse('tutor-list')
        data = {
            'user': self.user_tutor.id
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_admin)
        response = self.client.post(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Tutor.objects.all().count())

    def test_delete(self):
        tutor = Tutor.objects.create(user_id=self.user_tutor.id)
        self.assertEqual(1, Tutor.objects.all().count())

        url = reverse('tutor-detail', args=(tutor.id,))
        self.client.force_login(self.user_admin)
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Tutor.objects.all().count())

    def test_permissions(self):
        tutor = Tutor.objects.create(user_id=self.user_tutor.id)
        data = {
            'user': self.user_tutor.id
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_tutor)

        methods_list = ['post', 'put', 'delete']
        for method in methods_list:
            if method == 'post':
                url = reverse('tutor-list')
                response = self.client.post(url, data=json_data, content_type='application/json')
            if method == 'put':
                url = url = reverse('tutor-detail', args=(tutor.id,))
                response = self.client.put(url, data=json_data, content_type='application/json')
            if method == 'delete':
                url = url = reverse('tutor-detail', args=(tutor.id,))
                response = self.client.delete(url)
            self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class StudentApiTestCase(APITestCase):
    def setUp(self):
        self.user_tutor = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Sidorov', role=Role.TUTOR)
        self.user_student = User.objects.create(username='user2', password='user2', first_name='Ivan', last_name='Petrov', role=Role.STUDENT)
        self.user_admin = User.objects.create(username='user3', password='user3', first_name='Ivan', last_name='Ivanov', role=Role.ADMIN)
        tutor = Tutor.objects.create(user_id=self.user_tutor.id)

        self.subject1 = Subject.objects.create(name='Социология')
        self.course = Course.objects.create(name='Психология', tutor_id=tutor.id)
        self.course.subjects.add(self.subject1)

        self.study_group = StudyGroup.objects.create(name='q-2', course_id=self.course.id)


    def test_get_list(self):
        student = Student.objects.create(user_id=self.user_student.id, gender=Gender.MALE, study_group_id=self.study_group.id)

        url = reverse('student-list')
        response = self.client.get(url)

        serializer_data = StudentReadSerializer([student], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_item(self):
        student = Student.objects.create(user_id=self.user_student.id, gender=Gender.MALE, study_group_id=self.study_group.id)

        url = reverse('student-detail', args=(student.id,))
        response = self.client.get(url)

        serializer_data = StudentReadSerializer(student).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(0, Student.objects.all().count())
        url = reverse('student-list')
        data = {
            'user': self.user_student.id,
            'gender': 'MALE',
            'study_group': None
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_tutor)
        response = self.client.post(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Student.objects.all().count())

    def test_update(self):
        student = Student.objects.create(user_id=self.user_student.id, gender=Gender.MALE, study_group_id=None)

        url = reverse('student-detail', args=(student.id,))
        data = {
            'user': self.user_student.id,
            'gender': 'MALE',
            'study_group': self.study_group.id
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_tutor)
        response = self.client.put(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        student.refresh_from_db()
        self.assertEqual('q-2', self.study_group.name)

    def test_delete(self):
        student = Student.objects.create(user_id=self.user_student.id, gender=Gender.MALE, study_group_id=None)
        self.assertEqual(1, Student.objects.all().count())

        url = reverse('student-detail', args=(student.id,))
        self.client.force_login(self.user_tutor)
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Student.objects.all().count())

    def test_permissions(self):
        student = Student.objects.create(user_id=self.user_student.id, gender=Gender.MALE, study_group_id=None)
        data = {
            'user': self.user_student.id,
            'gender': 'MALE',
            'study_group': None
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_admin)

        methods_list = ['post', 'put', 'delete']
        for method in methods_list:
            if method == 'post':
                url = reverse('student-list')
                response = self.client.post(url, data=json_data, content_type='application/json')
            if method == 'put':
                url = url = reverse('student-detail', args=(student.id,))
                response = self.client.put(url, data=json_data, content_type='application/json')
            if method == 'delete':
                url = url = reverse('student-detail', args=(student.id,))
                response = self.client.delete(url)
            self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class SubjectApiTestCase(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Petrov', role=Role.ADMIN)
        self.user_tutor = User.objects.create(username='user2', password='user2', first_name='Ivan', last_name='Sidorov', role=Role.TUTOR)
        self.subject1 = Subject.objects.create(name='Социология')
        self.subject2 = Subject.objects.create(name='Философия')

    def test_get_list(self):
        url = reverse('subject-list')
        response = self.client.get(url)

        subjects = Subject.objects.all()
        serializer_data = SubjectSerializer(subjects, many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_item(self):
        url = reverse('subject-detail', args=(self.subject1.id,))
        response = self.client.get(url)

        subject = Subject.objects.get(id=self.subject1.id)
        serializer_data = SubjectSerializer(subject).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(2, Subject.objects.all().count())
        url = reverse('subject-list')
        data = {
            'name': 'Литература'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_admin)
        response = self.client.post(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Subject.objects.all().count())

    def test_update(self):
        url = reverse('subject-detail', args=(self.subject1.id,))
        data = {
            'name': 'Зарубежная литература'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_admin)
        response = self.client.put(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.subject1.refresh_from_db()
        self.assertEqual('Зарубежная литература', self.subject1.name)

    def test_delete(self):
        self.assertEqual(2, Subject.objects.all().count())
        url = reverse('subject-detail', args=(self.subject1.id,))
        self.client.force_login(self.user_admin)
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(1, Subject.objects.all().count())

    def test_permissions(self):
        data = {
            'name': 'Литература'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_tutor)

        methods_list = ['post', 'put', 'delete']
        for method in methods_list:
            if method == 'post':
                url = reverse('subject-list')
                response = self.client.post(url, data=json_data, content_type='application/json')
            if method == 'put':
                url = url = reverse('subject-detail', args=(self.subject1.id,))
                response = self.client.put(url, data=json_data, content_type='application/json')
            if method == 'delete':
                url = url = reverse('subject-detail', args=(self.subject1.id,))
                response = self.client.delete(url)
            self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class CourseApiTestCase(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Petrov', role=Role.ADMIN)
        self.user_tutor = User.objects.create(username='user2', password='user2', first_name='Ivan', last_name='Sidorov', role=Role.TUTOR)
        self.tutor = Tutor.objects.create(user_id=self.user_tutor.id)
        self.subject1 = Subject.objects.create(name='Социология')
        self.subject2 = Subject.objects.create(name='Философия')
        self.course = Course.objects.create(name='Психология', tutor_id=self.tutor.id)
        self.course.subjects.add(self.subject1)
        self.course.subjects.add(self.subject2)

    def test_get_list(self):
        url = reverse('course-list')
        response = self.client.get(url)

        serializer_data = CourseSerializer([self.course], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_item(self):
        url = reverse('course-detail', args=(self.course.id,))
        response = self.client.get(url)

        course = Course.objects.get(id=self.course.id)
        serializer_data = CourseSerializer(course).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(1, Course.objects.all().count())
        url = reverse('course-list')
        data = {
            'id': self.course.id,
            'name': 'Психология',
                'tutor': {
                    'user': {
                        'id': self.user_tutor.id,
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov',
                    }
                },
                'subjects': [
                    {
                        'id': self.subject1.id,
                        'name': 'Социология'
                    },
                    {
                        'id': self.subject2.id,
                        'name': 'Философия'
                    }
                ]
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_admin)
        response = self.client.post(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Course.objects.all().count())

    def test_update(self):
        url = reverse('course-detail', args=(self.course.id,))
        data = {
            'name': 'Психология семьи'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_admin)
        response = self.client.put(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.course.refresh_from_db()
        self.assertEqual('Психология семьи', self.course.name)

    def test_delete(self):
        self.assertEqual(1, Course.objects.all().count())
        url = reverse('course-detail', args=(self.course.id,))
        self.client.force_login(self.user_admin)
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Course.objects.all().count())

    def test_permissions(self):
        data = {
            'id': self.course.id,
            'name': 'Психология',
            'tutor': {
                'user': {
                    'id': self.user_tutor.id,
                    'first_name': 'Ivan',
                    'last_name': 'Sidorov',
                }
            },
            'subjects': [
                {
                    'id': self.subject1.id,
                    'name': 'Социология'
                },
                {
                    'id': self.subject2.id,
                    'name': 'Философия'
                }
            ]
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_tutor)

        methods_list = ['post', 'put', 'delete']
        for method in methods_list:
            if method == 'post':
                url = reverse('course-list')
                response = self.client.post(url, data=json_data, content_type='application/json')
            if method == 'put':
                url = url = reverse('course-detail', args=(self.course.id,))
                response = self.client.put(url, data=json_data, content_type='application/json')
            if method == 'delete':
                url = url = reverse('course-detail', args=(self.course.id,))
                response = self.client.delete(url)
            self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class StudyGroupApiTestCase(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Petrov', role=Role.ADMIN)
        self.user_tutor = User.objects.create(username='user2', password='user2', first_name='Ivan', last_name='Sidorov', role=Role.TUTOR)
        self.tutor = Tutor.objects.create(user_id=self.user_tutor.id)
        self.subject1 = Subject.objects.create(name='Социология')
        self.subject2 = Subject.objects.create(name='Философия')
        self.course = Course.objects.create(name='Психология', tutor_id=self.tutor.id)
        self.course.subjects.add(self.subject1)
        self.course.subjects.add(self.subject2)

        self.study_group = StudyGroup.objects.create(name='q-2', course_id=self.course.id)

    def test_get_list(self):
        url = reverse('studygroup-list')
        response = self.client.get(url)
        serializer_data = StudyGroupSerializer([self.study_group], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_item(self):
        url = reverse('studygroup-detail', args=(self.study_group.id,))
        response = self.client.get(url)

        study_group = StudyGroup.objects.get(id=self.study_group.id)
        serializer_data = StudyGroupSerializer(study_group).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(1, StudyGroup.objects.all().count())
        url = reverse('studygroup-list')
        data = {
            'name': 'q-2',
            'course': {
                'id': self.course.id,
                'name': 'Психология',
                'tutor': {
                    'user': {
                        'id': self.user_tutor.id,
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov'
                    }
                },
                'subjects': [
                    {
                        'id': self.subject1.id,
                        'name': 'Социология'
                    },
                    {
                        'id': self.subject2.id,
                        'name': 'Философия'
                    }
                ]
            }
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_tutor)
        response = self.client.post(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, StudyGroup.objects.all().count())

    def test_update(self):
        url = reverse('studygroup-detail', args=(self.study_group.id,))
        data = {
            'name': 'q-3'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_tutor)
        response = self.client.put(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.study_group.refresh_from_db()
        self.assertEqual('q-3', self.study_group.name)

    def test_delete(self):
        self.assertEqual(1, StudyGroup.objects.all().count())
        url = reverse('studygroup-detail', args=(self.study_group.id,))
        self.client.force_login(self.user_tutor)
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, StudyGroup.objects.all().count())

    def test_permissions(self):
        data = {
            'name': 'q-2',
            'course': {
                'id': self.course.id,
                'name': 'Психология',
                'tutor': {
                    'user': {
                        'id': self.user_tutor.id,
                        'first_name': 'Ivan',
                        'last_name': 'Sidorov'
                    }
                },
                'subjects': [
                    {
                        'id': self.subject1.id,
                        'name': 'Социология'
                    },
                    {
                        'id': self.subject2.id,
                        'name': 'Философия'
                    }
                ]
            }
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_admin)

        methods_list = ['post', 'put', 'delete']
        for method in methods_list:
            if method == 'post':
                url = reverse('studygroup-list')
                response = self.client.post(url, data=json_data, content_type='application/json')
            if method == 'put':
                url = url = reverse('studygroup-detail', args=(self.study_group.id,))
                response = self.client.put(url, data=json_data, content_type='application/json')
            if method == 'delete':
                url = url = reverse('studygroup-detail', args=(self.study_group.id,))
                response = self.client.delete(url)
            self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)


class ReportApiTestCase(APITestCase):
    def setUp(self):
        self.user_admin = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Petrov', role=Role.ADMIN)
        self.user_tutor = User.objects.create(username='user2', password='user2', first_name='Ivan', last_name='Sidorov', role=Role.TUTOR)
        self.report = Report.objects.create(type=ReportType.COURSE, status=Status.CREATED, created_at=datetime.now(), file=None)

    def test_get_list(self):
        url = reverse('report-list')
        response = self.client.get(url)
        serializer_data = ReportSerializer([self.report], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_item(self):
        url = reverse('report-detail', args=(self.report.id,))
        response = self.client.get(url)

        serializer_data = ReportSerializer(self.report).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(1, Report.objects.all().count())
        url = reverse('report-list')
        data = {
            'id': 2,
            'type': ReportType.GROUP,
            'status': Status.CREATED,
            'created_at': datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S"),
            'file': None
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_admin)
        response = self.client.post(url, data=json_data, content_type='application/json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Report.objects.all().count())

    def test_create_duplicate(self):
        url = reverse('report-list')
        data = {
            'id': 2,
            'type': ReportType.COURSE,
            'status': Status.CREATED,
            'created_at': datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S"),
            'file': None
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_admin)

        try:
            response = self.client.post(url, data=json_data, content_type='application/json')
        except IntegrityError:
            pass

    def test_delete(self):
        self.assertEqual(1, Report.objects.all().count())
        url = reverse('report-detail', args=(self.report.id,))
        self.client.force_login(self.user_admin)
        response = self.client.delete(url)
        
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Report.objects.all().count())

    def test_permissions(self):
        data = {
            'id': 2,
            'type': ReportType.GROUP,
            'status': Status.CREATED,
            'created_at': datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%S"),
            'file': None
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user_tutor)

        methods_list = ['post', 'delete']
        for method in methods_list:
            if method == 'post':
                url = reverse('report-list')
                response = self.client.post(url, data=json_data, content_type='application/json')
            if method == 'delete':
                url = url = reverse('report-detail', args=(self.report.id,))
                response = self.client.delete(url)
            self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)