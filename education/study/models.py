from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.TextChoices):
    ADMIN = 'admin', 'админ'
    TUTOR = 'tutor', 'куратор'
    STUDENT = 'student', 'студент'


class Gender(models.TextChoices):
    MALE = 'MALE', 'мужской'
    FEMALE = 'FEMALE', 'женский'


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
