from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User, Tutor, Student, StudyGroup, Subject, Course, Report


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class TutorReadSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Tutor
        fields = ('user', )


class TutorWriteSerializer(ModelSerializer):
    class Meta:
        model = Tutor
        fields = ('user', )


class SubjectSerializer(ModelSerializer):
    class Meta: 
        model = Subject
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    tutor = TutorReadSerializer()
    subjects = SubjectSerializer(many=True)
    class Meta: 
        model = Course
        fields = ('id', 'name', 'tutor', 'subjects')


class StudyGroupSerializer(ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = StudyGroup
        fields = ('name', 'course')


class StudentReadSerializer(ModelSerializer):
    user = UserSerializer()
    study_group = StudyGroupSerializer()
    class Meta:
        model = Student
        fields = ('user', 'gender', 'study_group')


class StudentWriteSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ('user', 'gender', 'study_group')


class ReportSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Report
        fields = '__all__'
