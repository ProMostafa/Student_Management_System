from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
# Create your models here.

# THE Important Part In Createing Custom User Is Add  THis In Setting.py 
#AUTH_USER_MODEL="userprofile.UserProfile"


class UserProfileManager(BaseUserManager):

    def create_user(self,email,first_name,last_name,password=None):
        if not email:
            raise ValueError('UserProfile Must Hane An Email !!!')


        email=self.normalize_email(email)
        user=self.model(email=email,first_name=first_name,last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,first_name,last_name,password):

        user=self.create_user(email,first_name,last_name,password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user



TYPE=(('Instructor','Instructor'),('Student','Student'))
class UserProfile(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=255 ,unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)


    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['first_name','last_name']

    objects=UserProfileManager()


    def get_full_name(self):
        return self.first_name+"  "+self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email



LEVEL=(('First_Year','First_Year'),
('Second_Year','Second Year'),
('Third_Year','Third_Year'),
('Fourth_Year','Fourth_Year'))

GENDER=(('Male','Male'),('Famale','Famale'))



def gpa_validate(value):
    if value > 4.0 :
        raise ValidationError(_('%(value)s is large than 4.0'),params={'value':value})
    elif value < 1.0:
        raise ValidationError(_('%(value)s is small than 1.0'),params={'value':value})



class Student_Info(models.Model):

    user_profile=models.OneToOneField(
        UserProfile,on_delete=models.CASCADE
    )
    type=models.CharField(choices=TYPE,default='Student',max_length=12)
    address=models.CharField(max_length=255,null=True,blank=True)
    phone=models.CharField(max_length=14,null=False)
    University_ID=models.CharField(max_length=3,null=False)
    level=models.CharField(choices=LEVEL,default='First_Year',max_length=12)
    gpa=models.FloatField(default=0.0,validators=[gpa_validate],help_text="Enter Correcr GPA Value")
    gender=models.CharField( choices=GENDER,default='Male',max_length=7)


    class Meta:
        ordering=['University_ID','level','gpa']

    def __str__(self):
        return "Student Name : {} {} ,Student_ID : {}".format(self.user_profile.first_name,self.user_profile.last_name,self.University_ID)

COURSES=(
    ('IT Fondamental','IT Fondamental'),
    ('CS Fondamental','CS Fondamental'),
    ('Mathematics_1','Mathematics_1'),
    ('Discrete Mathematics','Discrete Mathematics'),
    ('C++ Programming','C++ Programming'),
    ('Java Programming','Java Programming'),
    ('Python Programming','Python Programming'),
    ('C++ Advanced','C++ Advanced'),
    ('Java Advanced','Java Advanced'),
    ('Python Advanced','Python Advanced')
)
CREDITS_HOURS=(
    ('3 hours','3 hours'),
    ('2 hours','2 hours'),
    ('1 hours','1 hours')
)
class Courses(models.Model):
    #student=models.ManyToManyField(Student_Info,on_delete=models.CASCADE)
    course_name=models.CharField(choices=COURSES,default='Mathematics_1',max_length=20,primary_key=True,null=False)
    credit_hours=models.CharField(choices=CREDITS_HOURS,default='3 hours',max_length=8)
    #prerquesrt=models.CharField()

    def __str__(self):
        return "Course_Name: {}".format(self.course_name)


DEPARTMENT=(
    ('CS','CS'),
    ('IT','IT'),
    ('MM','MM'),
    ('IS','IS')
)

INSTRACTOR_LEVEL=(
    ('Fresh','Fresh'),
    ('Junior','Junior'),
    ('Senior','Senior'),
    ('Expert','Expert')
)

def age_validate(value):
    if value < 23 :
        raise ValidationError("Age Must Be 23 Or larger For Fresh Instructor !!!")
    elif value <0:
        raise ValidationError("Age Must Be Postive Value !!!")


class Instructor(models.Model):
    user_profile=models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    Type=models.CharField(choices=TYPE,default='Instructor',max_length=12 )
    department=models.CharField(choices=DEPARTMENT,max_length=2,default='CS')
    age=models.IntegerField(validators=[age_validate],default=23)
    phone=models.CharField(max_length=13)
    instructor_level=models.CharField(choices=INSTRACTOR_LEVEL,default='Fresh',max_length=7)


    def __str__(self):
        return 'Instructor Name: {} {}'.format(self.user_profile.first_name,self.user_profile.last_name)

class Instructor_Courses(models.Model):
    instructor_profile=models.ForeignKey(Instructor,on_delete=models.CASCADE)
    course=models.ForeignKey(Courses,on_delete=models.CASCADE)
    number_off_student=models.IntegerField(default='100')
    start_date=models.DateField()
    end_date=models.DateField()

    def __str__(self):
        name=self.instructor_profile.user_profile.first_name+" "+self.instructor_profile.user_profile.last_name
        return "Instructor Name: {} , Course Name: {}".format(name,self.course)
   



class Student_Register(models.Model):
    student=models.ForeignKey(Student_Info,on_delete=models.DO_NOTHING)
    courses=models.ForeignKey(Instructor_Courses,on_delete=models.DO_NOTHING)
    register_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return "Student: {} Register In Course {}".format(self.student.user_profile.first_name,self.courses)