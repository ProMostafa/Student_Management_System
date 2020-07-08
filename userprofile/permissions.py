from rest_framework import permissions
from .models import Student_Info , Instructor
from django.shortcuts import get_object_or_404 

class UpdateOwnProfile(permissions.BasePermission):

    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.id == obj.id 


class UpdateOwnStudent_Info(permissions.BasePermission):

    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.id == obj.user_profile.id

class InstructorOnlyAccess(permissions.BasePermission):
    message="Instructor Only Access This APi ,Please Login AS Instructor !!!"

    def has_permission(self,request,view):
        try:
            obj=get_object_or_404(Instructor,user_profile=request.user.id)
            return True
        except:
            return False


class Students_Access_Denied(permissions.BasePermission):
    message="Access Denied For Students !!!"
    def has_permission(self,request,view):
        try:
            obj=get_object_or_404(Student_Info,user_profile=request.user.id)
            return False
        except:
            return True


class UpdateOwnInstructorProfile(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user.id == obj.user_profile.id
