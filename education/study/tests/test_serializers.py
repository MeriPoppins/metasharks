from django.test import TestCase

from study.models import User, Tutor, Student, StudyGroup, Subject, Course
from study.selializers import UserSerializer, TutorSerializer, SubjectSerializer, CourseSerializer,\
                            StudyGroupSerializer, StudentSerializer


class UsersSerializersTestCase(TestCase):
    def test_ok(self):
        user = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
        data = UserSerializer([user], many=True).data
        expected_data = [
            {
                'first_name': 'Ivan',
                'last_name': 'Petrov'
            }
        ]
        self.assertEqual(expected_data, data)


class TutorSerializersTestCase(TestCase):
    def test_ok(self):
        user = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
        tutor = Tutor.objects.create(user_id=user.id)
        data = TutorSerializer([tutor], many=True).data
        expected_data = [
            {
                'user': {
                    'first_name': 'Ivan',
                    'last_name': 'Petrov'
                }
            }
        ]
        self.assertEqual(expected_data, data)


class SubjectSerializerTestCase(TestCase):
    def test_ok(self):
        subject = Subject.objects.create(name='Социология')
        data = SubjectSerializer([subject], many=True).data
        expected_data = [
            {
                'id': subject.id,
                'name': 'Социология'
            }
        ]
        self.assertEqual(expected_data, data)


class CourseSerializerTestCase(TestCase):
    def test_ok(self):
        user = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
        tutor = Tutor.objects.create(user_id=user.id)

        subject1 = Subject.objects.create(name='Социология')
        subject2 = Subject.objects.create(name='Статистика')
        course = Course.objects.create(name='Психология', tutor_id=tutor.id)
        course.subjects.add(subject1)
        course.subjects.add(subject2)

        data = CourseSerializer([course], many=True).data
        expected_data = [
            {
                'name': 'Психология',
                'tutor': {
                    'user': {
                        'first_name': 'Ivan',
                        'last_name': 'Petrov'
                    }
                },
                'subjects': [
                    {
                        'id': subject1.id,
                        'name': 'Социология'
                    },
                    {
                        'id': subject2.id,
                        'name': 'Статистика'
                    }
                ]
            }
        ]
        self.assertEqual(expected_data, data)


class StudyGroupSerializerTestCase(TestCase):
    def test_ok(self):
        user = User.objects.create(username='user1', first_name='Ivan', last_name='Petrov')
        tutor = Tutor.objects.create(user_id=user.id)

        subject1 = Subject.objects.create(name='Социология')
        subject2 = Subject.objects.create(name='Статистика')
        course = Course.objects.create(name='Психология', tutor_id=tutor.id)
        course.subjects.add(subject1)
        course.subjects.add(subject2)

        study_group = StudyGroup.objects.create(name='q-2', course_id=course.id)

        data = StudyGroupSerializer([study_group], many=True).data
        expected_data = [
            {
                'name': 'q-2',
                'course': {
                    'name': 'Психология',
                    'tutor': {
                        'user': {
                            'first_name': 'Ivan',
                            'last_name': 'Petrov'
                        }
                    },
                    'subjects': [
                        {
                            'id': subject1.id,
                            'name': 'Социология'
                        },
                        {
                            'id': subject2.id,
                            'name': 'Статистика'
                        }
                    ]
                }
            }
        ]
        self.assertEqual(expected_data, data)

class StudentSerializerTestCase(TestCase):
    def test_ok(self):
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

        data = StudentSerializer([student], many=True).data
        expected_data = [
            {
                'user': {
                    'first_name': 'Ivan',
                    'last_name': 'Sidorov'
                },
                'gender': 'MALE',
                'study_group': {
                    'name': 'q-2',
                    'course': {
                        'name': 'Психология',
                        'tutor': {
                            'user': {
                                'first_name': 'Ivan',
                                'last_name': 'Petrov'
                            }
                        },
                        'subjects': [
                            {
                                'id': subject1.id,
                                'name': 'Социология'
                            },
                            {
                                'id': subject2.id,
                                'name': 'Статистика'
                            }
                        ]
                    }
                }
            }
        ]
        self.assertEqual(expected_data, data)
