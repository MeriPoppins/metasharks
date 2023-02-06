"""education URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter

from study.api.v1.courses import CourseViewSet, SubjectViewSet, StudyGroupViewSet, ReportViewSet
from study.api.v1.users import UserViewSet, TutorViewSet, StudentViewSet


router = SimpleRouter()

router.register('api/v1/users', UserViewSet)
router.register('api/v1/tutors', TutorViewSet)
router.register('api/v1/students', StudentViewSet)
router.register('api/v1/courses', CourseViewSet)
router.register('api/v1/subjects', SubjectViewSet)
router.register('api/v1/study_groups', StudyGroupViewSet)
router.register('api/v1/reports', ReportViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += router.urls
