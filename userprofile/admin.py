from django.contrib import admin
from .models import UserProfile ,Student_Info ,Courses,Instructor ,Instructor_Courses ,Student_Register

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Student_Info)
admin.site.register(Courses)
admin.site.register(Instructor)
admin.site.register(Instructor_Courses)
admin.site.register(Student_Register)
