from rest_framework.viewsets import ModelViewSet

from study.models import User, Tutor, Student
from study.selializers import UserSerializer, TutorSerializer, StudentSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TutorViewSet(ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer