from django.contrib import admin
from  .models import *
# Register your models here.
# from .models import Question
# admin.site.register(Question)

admin.site.register(Class)
admin.site.register(Teachers)
admin.site.register(Students)
admin.site.register(Module)
admin.site.register(Seance)
admin.site.register(Presence)