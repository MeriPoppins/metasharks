from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from study.models import Course, Subject, StudyGroup, User, Tutor
from study.selializers import CourseSerializer, SubjectSerializer, StudyGroupSerializer
from study.permissions import IsAdmin, IsTutor


class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all().order_by('name')
    serializer_class = SubjectSerializer
    permission_classes = [IsAdmin]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all().select_related('tutor').prefetch_related('subjects').order_by('name')
    serializer_class = CourseSerializer
    permission_classes = [IsAdmin]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            tutor = Tutor.objects.get(user_id=request.data['tutor']['user']['id'])
        except Tutor.DoesNotExist:
            raise ValidationError({'message': 'Tutot does not exist'})

        course = Course.objects.create(
            name=request.data['name'],
            tutor=tutor
        )

        for subject_data in request.data['subjects']:
            try:
                subject = Subject.objects.get(pk=subject_data['id'])
            except Subject.DoesNotExist:
                raise ValidationError({'message': 'Subject does not exist'})
            course.subjects.add(subject)

        headers = self.get_success_headers(request.data)
        return Response(request.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
        

class StudyGroupViewSet(ModelViewSet):
    queryset = StudyGroup.objects.all()
    serializer_class = StudyGroupSerializer
    permission_classes = [IsTutor]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            course = Course.objects.get(id=request.data['course']['id'])
        except Course.DoesNotExist:
            raise ValidationError({'message': 'Course does not exist'})

        study_group = StudyGroup.objects.create(
            name=request.data['name'],
            course=course
        )

        headers = self.get_success_headers(request.data)
        return Response(request.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
