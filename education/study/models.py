from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Role(models.TextChoices):
    ADMIN = 'admin', 'админ'
    TUTOR = 'tutor', 'куратор'
    STUDENT = 'student', 'студент'


class Gender(models.TextChoices):
    MALE = 'MALE', 'мужской'
    FEMALE = 'FEMALE', 'женский'


class ReportType(models.TextChoices):
    COURSE = 'course_report', 'отчет о направлениях'
    GROUP = 'groups_report', 'отчет о группах'


class Status(models.TextChoices):
    CREATED = 'created', 'создан'
    PROCESSED = 'processed', 'обрабатывается'
    FALIED = 'falied', 'завершен с ошибкой'
    COMPLETED = 'completed', 'завершен успешно'


class User(AbstractUser):
    role = models.CharField(max_length=50, choices=Role.choices, null=True, blank=True, verbose_name='Статус пользователя')


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Куратор'
        verbose_name_plural = 'Кураторы'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50, choices=Gender.choices, default=Gender.MALE, verbose_name='Пол')
    study_group = models.ForeignKey('StudyGroup', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Учебная группа')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'


class StudyGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название группы')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'


class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название дисциплины')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'


class Course(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название курса')
    tutor = models.ForeignKey(Tutor, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Куратор')
    subjects = models.ManyToManyField(Subject, related_name='course_subjects')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Report(models.Model):
    type = models.CharField(max_length=50, choices=ReportType.choices, default=ReportType.COURSE, verbose_name='Тип отчета')
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.CREATED, verbose_name='Статус отчета')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    file = models.FileField(upload_to=f'reports/', verbose_name='Ссылка на скачивание', blank=True, null=True)

    def __str__(self):
        return f'{self.type} {self.created_at}'

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = 'Отчеты'
        constraints = [
            models.UniqueConstraint(fields=['type'], condition=(Q(status=Status.CREATED) | Q(status=Status.PROCESSED)), name='unique_status_type')
        ]


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
