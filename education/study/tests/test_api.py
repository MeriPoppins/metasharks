import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from study.models import User, Tutor, Student, StudyGroup, Subject, Course, Role, Gender
from study.selializers import UserSerializer, TutorSerializer, SubjectSerializer, CourseSerializer,\
                            StudyGroupSerializer, StudentSerializer


# class UsersApiTestCase(APITestCase):
#     def test_get_list(self):
#         user = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
#         url = reverse('user-list')
#         response = self.client.get(url)
#         serializer_data = UserSerializer([user], many=True).data
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.assertEqual(serializer_data, response.data)

# class TutorApiTestCase(APITestCase):
#     def test_get_list(self):
#         user = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
#         tutor = Tutor.objects.create(user_id=user.id)
#         url = reverse('tutor-list')
#         response = self.client.get(url)
#         serializer_data = TutorSerializer([tutor], many=True).data
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.assertEqual(serializer_data, response.data)


# class StudentApiTestCase(APITestCase):
#     def test_get_list(self):
#         user1 = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
#         user2 = User.objects.create(username='user2', first_name='Ivan', last_name='Sidorov')
#         tutor = Tutor.objects.create(user_id=user1.id)

#         subject1 = Subject.objects.create(name='Социология')
#         subject2 = Subject.objects.create(name='Статистика')
#         course = Course.objects.create(name='Психология', tutor_id=tutor.id)
#         course.subjects.add(subject1)
#         course.subjects.add(subject2)

#         study_group = StudyGroup.objects.create(name='q-2', course_id=course.id)
#         student = Student.objects.create(user_id=user2.id, gender='MALE', study_group_id=study_group.id)

#         url = reverse('student-list')
#         response = self.client.get(url)
#         serializer_data = StudentSerializer([student], many=True).data
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.assertEqual(serializer_data, response.data)


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
