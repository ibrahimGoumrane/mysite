from django.contrib import admin
from django.urls import include, path
from . import views
app_name='mysite'
urlpatterns=[
    # path('',views.index,name='index'),
    path('',views.home,name= 'home'),
    path('face_recognizer/',views.face_recognizer,name='face_recognizer'),
    path('student_info/<int:student_id>',views.student_info,name='student_info'),
]