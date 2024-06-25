from django.contrib import admin
from django.urls import include, path
from . import views
app_name='FaceRecoProj'
urlpatterns=[
    path('',views.home,name= 'home'),
    path('FaceRecoApp/',views.face_recognizer,name='FaceRecoApp'),
    path('FaceRecoApp/modules',views.class_modules,name='class_modules'),
    path('student_info/<int:student_id>',views.student_info,name='student_info'),
    path('result_submission/',views.result_submission,name='result_submission'),
    path('FaceRecoApp/updateStatus',views.updateStatus,name='updateStatus'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]