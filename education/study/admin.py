from django.contrib import admin

from .models import User, Tutor, Student, StudyGroup, Subject, Course, Report


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Tutor)
class TutorAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    pass
