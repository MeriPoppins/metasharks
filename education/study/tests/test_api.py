from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from study.models import User, Tutor, Student, StudyGroup, Subject, Course
from study.selializers import UserSerializer, TutorSerializer, SubjectSerializer, CourseSerializer,\
                            StudyGroupSerializer, StudentSerializer


class UsersApiTestCase(APITestCase):
    def test_get_list(self):
        user = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
        url = reverse('user-list')
        response = self.client.get(url)
        serializer_data = UserSerializer([user], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

class TutorApiTestCase(APITestCase):
    def test_get_list(self):
        user = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
        tutor = Tutor.objects.create(user_id=user.id)
        url = reverse('tutor-list')
        response = self.client.get(url)
        serializer_data = TutorSerializer([tutor], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


class SubjectApiTestCase(APITestCase):
    def test_get_list(self):
        subject = Subject.objects.create(name='Социология')
        url = reverse('subject-list')
        response = self.client.get(url)
        serializer_data = SubjectSerializer([subject], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


class CourseApiTestCase(APITestCase):
    def test_get_list(self):
        user = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
        tutor = Tutor.objects.create(user_id=user.id)

        subject1 = Subject.objects.create(name='Социология')
        subject2 = Subject.objects.create(name='Статистика')
        course = Course.objects.create(name='Психология', tutor_id=tutor.id)
        course.subjects.add(subject1)
        course.subjects.add(subject2)

        url = reverse('course-list')
        response = self.client.get(url)
        serializer_data = CourseSerializer([course], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


class StudyGroupApiTestCase(APITestCase):
    def test_get_list(self):
        user = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
        tutor = Tutor.objects.create(user_id=user.id)

        subject1 = Subject.objects.create(name='Социология')
        subject2 = Subject.objects.create(name='Статистика')
        course = Course.objects.create(name='Психология', tutor_id=tutor.id)
        course.subjects.add(subject1)
        course.subjects.add(subject2)

        study_group = StudyGroup.objects.create(name='q-2', course_id=course.id)

        url = reverse('studygroup-list')
        response = self.client.get(url)
        serializer_data = StudyGroupSerializer([study_group], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)


class StudentApiTestCase(APITestCase):
    def test_get_list(self):
        user1 = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
        user2 = User.objects.create(username='user2', first_name='Ivan', last_name='Sidorov')
        tutor = Tutor.objects.create(user_id=user1.id)

        subject1 = Subject.objects.create(name='Социология')
        subject2 = Subject.objects.create(name='Статистика')
        course = Course.objects.create(name='Психология', tutor_id=tutor.id)
        course.subjects.add(subject1)
        course.subjects.add(subject2)

        study_group = StudyGroup.objects.create(name='q-2', course_id=course.id)
        student = Student.objects.create(user_id=user2.id, gender='MALE', study_group_id=study_group.id)

        url = reverse('student-list')
        response = self.client.get(url)
        serializer_data = StudentSerializer([student], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
