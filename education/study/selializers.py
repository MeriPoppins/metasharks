from rest_framework.serializers import ModelSerializer

from .models import User, Tutor, Student, StudyGroup, Subject, Course


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


class TutorSerializer(ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Tutor
        fields = ('user', )


class SubjectSerializer(ModelSerializer):
    class Meta: 
        model = Subject
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    tutor = TutorSerializer()
    subjects = SubjectSerializer(many=True)
    class Meta: 
        model = Course
        fields = ('id', 'name', 'tutor', 'subjects')


class StudyGroupSerializer(ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = StudyGroup
        fields = ('name', 'course')


class StudentSerializer(ModelSerializer):
    user = UserSerializer()
    study_group = StudyGroupSerializer()
    class Meta:
        model = Student
        fields = ('user', 'gender', 'study_group')
