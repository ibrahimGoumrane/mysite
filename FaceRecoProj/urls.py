from django.contrib import admin
from django.urls import include, path,re_path 
from . import views

urlpatterns = [
    path('thankyou/',views.thankyou , name= 'thankyou'),
    path("admin/", admin.site.urls),
    path('',include('FaceRecoApp.urls'),name='FaceRecoApp'),
]
