from django.shortcuts import render
from django.http import HttpResponse,HttpRequest,HttpResponsePermanentRedirect,HttpResponseNotFound,HttpResponseRedirect
from pathlib import Path

from .forms import ContactForm ,SeanceData
from .models import Contact  ,UtilsData ,upload_location
from .detector import face_handler 


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
def face_recognizer(request: HttpRequest) -> HttpResponse:
    form = SeanceData()
    if request.method == 'POST':
        # print(request.POST,request.FILES)
        form = SeanceData(request.POST,request.FILES)
        print(form.errors) 
        if form.is_valid():
            # Extract cleaned data from the form
            module_name = form.cleaned_data['module_name']
            cycle = form.cleaned_data['cycle']
            cycle_prepa = form.cleaned_data['cycle_prepa'] 
            cycle_eng =form.cleaned_data['cycle_eng']
            filiere = form.cleaned_data['filiere']
            image = form.cleaned_data['image']
            # Create an instance of the Seance model
            seance_data=UtilsData.objects.create(
                module_name=module_name,
                cycle=cycle,
                cycle_eng=cycle_eng,
                cycle_prepa=cycle_prepa,
                filiere=filiere,
                image=image
            )
            img_path=Path('media').joinpath(Path(upload_location(seance_data,image)))
            print(img_path.absolute)
            face_handler.recognize_faces(img_path.absolute())

            # Redirect to a new URL after successful form submission
            return HttpResponseRedirect('/thankyou/')

    return render(request, 'face_recognizer.html', {'form': form})
def student_info(request , student_id):
    return render(request, 'student_info.html')
