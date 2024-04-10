from django.shortcuts import render
from django.http import HttpResponse,HttpRequest,HttpResponsePermanentRedirect,HttpResponseNotFound,HttpResponseRedirect


def thankyou(request):
    return render(request ,'thankyou.html')


