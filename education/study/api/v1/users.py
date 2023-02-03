from rest_framework.viewsets import ModelViewSet

from study.models import User, Tutor, Student
from study.selializers import UserSerializer, TutorReadSerializer, TutorWriteSerializer, StudentReadSerializer, StudentWriteSerializer
from study.permissions import IsOwnerOrStaff, IsAdmin, IsTutor


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrStaff]


class TutorViewSet(ModelViewSet):
    queryset = Tutor.objects.all()
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return TutorWriteSerializer

        return TutorReadSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [IsTutor]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return StudentWriteSerializer

        return StudentReadSerializer
