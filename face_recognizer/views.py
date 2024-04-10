from django.shortcuts import render
from django.http import HttpResponse,HttpRequest,HttpResponsePermanentRedirect,HttpResponseNotFound,HttpResponseRedirect

from .forms import ContactForm
from .models import Contact
# Create your views here.


def index(request):
    return render(request, 'index.html')
def home(request :HttpRequest)->HttpResponse:
    form = ContactForm()
    if request.method =='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            firstname = form.cleaned_data['firstName']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            description = form.cleaned_data['description']
            print(name, firstname, email, subject, description)
            Contact.objects.create(
                name=name,
                firstName=firstname,
                email=email,
                subject=subject,
                description=description,
            )
            # Redirect to a new URL after successful form submission
            return HttpResponseRedirect('/thankyou/')
    return render(request, 'home.html',{'form':form})
def face_recognizer(request):
    return render(request, 'face_recognizer.html')
def student_info(request , student_id):
    return render(request, 'student_info.html')
