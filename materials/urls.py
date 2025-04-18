from django.urls import path
from rest_framework.routers import SimpleRouter

from materials.views import LessonCreateAPIView, LessonListAPIView, LessonUpdateAPIView, LessonRetrieveAPIView, LessonDestroyAPIView
from materials.views import CourseViewSet

from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register('courses', CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson-retrieve'),
    path('lessons/create/', LessonCreateAPIView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lesson-destroy'),
    path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lesson-update')
]

urlpatterns += router.urls


