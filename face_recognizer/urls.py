from django.contrib import admin
from django.urls import include, path
from . import views
app_name='mysite'
urlpatterns=[
    path('',views.home,name= 'home'),
    path('face_recognizer/',views.face_recognizer,name='face_recognizer'),
    path('face_recognizer/modules',views.class_modules,name='class_modules'),
    path('student_info/<int:student_id>',views.student_info,name='student_info'),
    path('result_submission/',views.result_submission,name='result_submission'),
]