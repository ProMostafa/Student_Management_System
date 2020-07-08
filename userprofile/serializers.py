from rest_framework import serializers
from .models import UserProfile , Student_Info ,Courses ,Instructor ,Instructor_Courses ,Student_Register



class Student_InfoSerializer(serializers.ModelSerializer):

    class Meta:
        model=Student_Info
        fields=('id','user_profile','address','phone','University_ID','level','gpa','gender')
        #fields=('id','name','address','phone','University_ID','level','gpa','gender')
        extra_kwargs={'user_profile':{'read_only':True},
        'type':{'read_only':True}
        }
        

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model=UserProfile
        fields=('id','email','first_name','last_name','password')
        extra_kwargs={
            'password':{
                'write_only':True,
                'style':{'input_type':'password'}
            }
        }
    
    def create(self, validated_data):
        user=UserProfile.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )

        return user


class CoursesSerliazer(serializers.ModelSerializer):
    class Meta:
        model=Courses
        fields='__all__'



class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Instructor
        fields=('id','user_profile','Type','department','age','phone','instructor_level')
        extra_kwargs={'user_profile':{'read_only':True},
        'Type':{'read_only':True}
        }


class InstructorCoursesSerializer(serializers.ModelSerializer):

    class Meta:
        model=Instructor_Courses
        fields=('instructor_profile','course','number_off_student','start_date','end_date')
        extra_kwargs={'instructor_profile':{'read_only':True}}


class StudentRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model=Student_Register
        fields=('student','courses','register_date')