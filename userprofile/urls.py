from django.urls import path ,include
from rest_framework.routers import DefaultRouter
from userprofile import views

router=DefaultRouter()
router.register('userprofile',views.UserProfileAPIViewSet,basename='userprofile')
router.register('Instructor_Info',views.InstructorAPIView,basename='Instructor_Info')
router.register('Student_Info',views.StudentInfoAPI,basename='Student_Info')
router.register('Courses',views.CoursesAPIView,basename='Courses')
router.register('Instructor_Courses',views.Instructor_CoursesAPIView,basename='Instructor_Courses')
router.register('Student_Register_Courses',views.Student_RegisterAPIView,basename='Student_Register_Courses')


urlpatterns = [
     path('', include(router.urls)),
     path('login/',views.UserLoginAPIView.as_view()),
]
