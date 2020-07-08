from django.shortcuts import render
from rest_framework import viewsets
from .models import UserProfile ,Student_Info ,Courses ,Instructor ,Student_Register
from .serializers import UserProfileSerializer ,Student_InfoSerializer ,CoursesSerliazer ,InstructorSerializer
from .serializers import InstructorCoursesSerializer ,StudentRegisterSerializer
from .models import Instructor_Courses
from .permissions import UpdateOwnProfile ,UpdateOwnStudent_Info ,InstructorOnlyAccess ,UpdateOwnInstructorProfile
from .permissions import Students_Access_Denied
from rest_framework import filters
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework .authentication import TokenAuthentication
from rest_framework.permissions  import IsAuthenticatedOrReadOnly

# Create your views here.

class UserProfileAPIViewSet(viewsets.ModelViewSet):

    serializer_class=UserProfileSerializer
    queryset=UserProfile.objects.all()

    authentication_classes=(TokenAuthentication,)
    permission_classes=(UpdateOwnProfile,)

    filter_backends=(filters.SearchFilter,)
    search_fields=('email','first_name','last_name')

    

class StudentInfoAPI(viewsets.ModelViewSet):
    authentication_classes=(TokenAuthentication,)
    permission_classes=(UpdateOwnStudent_Info,
    )

    serializer_class=Student_InfoSerializer
    queryset=Student_Info.objects.all()
# Override create Object behavior 
#When save data without this method Error 
#NOT NULL constraint failed: userprofile_student_info.user_profile_id   (user_profile is missing and become null when sava data ERROR )

    def perform_create(self,serializer):
        # Assigment The Logged user_profle to user_porfile in(student_info model) 
       # if self.request.user.is_authenticated:
            # serializer.save(user_profile=self.request.user)
        #else:
        #  raise Exception("Must Login Frist Befor Register Your Informations !!!")   
        try:
            serializer.save(user_profile=self.request.user)
        except Exception as identifier:
            raise Exception("Must Login Frist Befor Register Your Informations !!!")


class UserLoginAPIView(ObtainAuthToken):
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES



class CoursesAPIView(viewsets.ModelViewSet):
    authentication_classes=(TokenAuthentication,)
    permission_classes=(InstructorOnlyAccess,)
    serializer_class=CoursesSerliazer
    queryset=Courses.objects.all()




class InstructorAPIView(viewsets.ModelViewSet):
    authentication_classes=(TokenAuthentication,)
    permission_classes=(Students_Access_Denied,UpdateOwnInstructorProfile,)
    serializer_class=InstructorSerializer
    queryset=Instructor.objects.all()
    
    def perform_create(self,serializer):
        if self.request.user.is_authenticated:
            serializer.save(user_profile=self.request.user)
        else:
            raise Exception("Must Login Frist Befor Register Your Informations !!!")

        
    


class Instructor_CoursesAPIView(viewsets.ModelViewSet):
     authentication_classes=(TokenAuthentication,)
     permission_classes=(InstructorOnlyAccess,)
     serializer_class=InstructorCoursesSerializer
     queryset=Instructor_Courses.objects.all()


     def perform_create(self,serializer):
        if self.request.user.is_authenticated:
            try:
                instructor=Instructor.objects.get(user_profile=self.request.user)
                serializer.save(instructor_profile=instructor)
            except:
                raise Exception("Must Login Frist Befor Register Your Informations !!!")




class Student_RegisterAPIView(viewsets.ModelViewSet):
    
    serializer_class=StudentRegisterSerializer
    queryset=Student_Register.objects.all()

