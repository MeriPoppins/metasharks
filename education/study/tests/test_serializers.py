from django.test import TestCase
from datetime import datetime

from study.models import User, Tutor, Student, StudyGroup, Subject, Course, Role, Gender, Report, ReportType, Status
from study.selializers import UserSerializer, TutorReadSerializer, TutorWriteSerializer, SubjectSerializer,\
                            CourseSerializer, StudyGroupSerializer, StudentReadSerializer, StudentWriteSerializer,\
                            ReportSerializer


class UsersSerializersTestCase(TestCase):
    def test_ok(self):
        user = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Petrov', role=Role.ADMIN)
        data = UserSerializer([user], many=True).data
        expected_data = [
            {
                'id': user.id,
                'first_name': 'Ivan',
                'last_name': 'Petrov'
            }
        ]
        self.assertEqual(expected_data, data)


class TutorReadSerializersTestCase(TestCase):
    def test_ok(self):
        user = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Petrov', role=Role.TUTOR)
        tutor = Tutor.objects.create(user_id=user.id)
        data = TutorReadSerializer([tutor], many=True).data
        expected_data = [
            {
                'user': {
                    'id': user.id,
                    'first_name': 'Ivan',
                    'last_name': 'Petrov'
                }
            }
        ]
        self.assertEqual(expected_data, data)


class TutorWriteSerializersTestCase(TestCase):
    def test_ok(self):
        user = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Petrov', role=Role.TUTOR)
        tutor = Tutor.objects.create(user_id=user.id)
        data = TutorWriteSerializer([tutor], many=True).data
        expected_data = [
            {
                'user': user.id,
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
        user = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Petrov', role=Role.TUTOR)
        tutor = Tutor.objects.create(user_id=user.id)

        subject1 = Subject.objects.create(name='Социология')
        subject2 = Subject.objects.create(name='Статистика')
        course = Course.objects.create(name='Психология', tutor_id=tutor.id)
        course.subjects.add(subject1)
        course.subjects.add(subject2)

        data = CourseSerializer([course], many=True).data
        expected_data = [
            {
                'id': course.id,
                'name': 'Психология',
                'tutor': {
                    'user': {
                        'id': user.id,
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
        user = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Petrov', role=Role.TUTOR)
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
                    'id': course.id,
                    'name': 'Психология',
                    'tutor': {
                        'user': {
                            'id': user.id,
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


class StudentReadSerializerTestCase(TestCase):
    def test_ok(self):
        user1 = User.objects.create(username='user1', password='user1', first_name='Ivan', last_name='Petrov', role=Role.TUTOR)
        user2 = User.objects.create(username='user2', password='user2', first_name='Ivan', last_name='Sidorov', role=Role.STUDENT)
        tutor = Tutor.objects.create(user_id=user1.id)

        subject1 = Subject.objects.create(name='Социология')
        subject2 = Subject.objects.create(name='Статистика')
        course = Course.objects.create(name='Психология', tutor_id=tutor.id)
        course.subjects.add(subject1)
        course.subjects.add(subject2)

        study_group = StudyGroup.objects.create(name='q-2', course_id=course.id)
        student = Student.objects.create(user_id=user2.id, gender=Gender.MALE, study_group_id=study_group.id)

        data = StudentReadSerializer([student], many=True).data
        expected_data = [
            {
                'user': {
                    'id': user2.id,
                    'first_name': 'Ivan',
                    'last_name': 'Sidorov'
                },
                'gender': 'MALE',
                'study_group': {
                    'name': 'q-2',
                    'course': {
                        'id': course.id,
                        'name': 'Психология',
                        'tutor': {
                            'user': {
                                'id': user1.id,
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


class StudentWriteSerializerTestCase(TestCase):
    def test_ok(self):
        user = User.objects.create(username='user', password='user', first_name='Ivan', last_name='Sidorov', role=Role.STUDENT)
        student = Student.objects.create(user_id=user.id, gender=Gender.MALE, study_group_id=None)

        data = StudentWriteSerializer([student], many=True).data
        expected_data = [
            {
                'user': user.id,
                'gender': 'MALE',
                'study_group': None
            }
        ]
        self.assertEqual(expected_data, data)


class ReportSerializersTestCase(TestCase):
    def test_ok(self):
        report = Report.objects.create(type=ReportType.COURSE, status=Status.CREATED, created_at=datetime.now(), file=None)
        data = ReportSerializer([report], many=True).data
        expected_data = [
            {
                'id': report.id,
                'type': ReportType.COURSE,
                'status': Status.CREATED,
                'created_at': datetime.strftime(report.created_at, "%Y-%m-%dT%H:%M:%S"),
                'file': None
            }
        ]
        self.assertEqual(expected_data, data)
