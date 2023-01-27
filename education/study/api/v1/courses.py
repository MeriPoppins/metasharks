from rest_framework.viewsets import ModelViewSet

from study.models import Course, Subject, StudyGroup
from study.selializers import CourseSerializer, SubjectSerializer, StudyGroupSerializer


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all().order_by('name')
    serializer_class = SubjectSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().select_related('tutor').prefetch_related('subjects').order_by('name')
    serializer_class = CourseSerializer


class StudyGroupViewSet(ModelViewSet):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
