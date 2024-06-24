from django.shortcuts import render
from django.http import JsonResponse,HttpResponse,HttpRequest,HttpResponsePermanentRedirect,HttpResponseNotFound,HttpResponseRedirect,HttpResponseServerError
from .DataManip.sgda_setters import data_base_setters
from .DataManip.sgda_getters import data_base_getters
from .forms import ContactForm ,SeanceData
from .models import Contact  ,UtilsData 
from .DetectorMain.utils import utils
from json import dumps ,loads




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
def class_modules(request:HttpRequest)->JsonResponse:
    try :
        if request.method=='POST':
            # Parse the JSON data from the request body
            json_data = loads(request.body)
            
            # Access the values from the JSON data
            cycle = json_data.get('cycle')
            cycle_year = json_data.get('cycleYear')
            cycle_filiere = json_data.get('cycleFiliere')
            #creating the class object using that data
            class_obj=data_base_getters.get_class(cycle=cycle,
                                                  cycle_year=cycle_year
                                                  ,filiere=cycle_filiere)
            #using the class obj in ordre to retreive the modules
            modules = data_base_getters.get_class_modules(
                class_id=class_obj.pk
            )
            sended_modules=[]
            
            for module in modules:
                sended_modules.append(module.module_name) 
                
            ###return the json reponse 
            print(sended_modules)
            return JsonResponse({
                'modules' : sended_modules,
            })
        else :
            raise Exception('the request is not Post')
    except Exception as e :
        stri = str(e)
        print('en error occured :' ,stri)
        return JsonResponse({'en error occured ' :stri},status=500) 
def face_recognizer(request: HttpRequest) -> HttpResponse:
    form = SeanceData()
    if request.method == 'POST':
        form = SeanceData(request.POST,request.FILES)
        module_name = request.POST['module_name']
        if form.is_valid():
            try :
                #contain all the data inputed from the user
                seance_data:UtilsData=utils.utilsdata_init(module_name , form)
                ###### get the year , filiere or section and cycle 
                year=1
                filiere=''
                if seance_data.cycle == 'cycle_ingenieur':
                    filiere = seance_data.filiere.lower()
                    year = seance_data.cycle_eng  
                else :
                    year=seance_data.cycle_prepa
                    filiere =seance_data.section.lower()
                year=int(year)

                ####### get the class , module and students 
                class_obj =data_base_getters.get_class(seance_data.cycle,year,filiere)
                module_obj=data_base_getters.get_module(class_obj.pk,seance_data.module_name)
                
                present_student:list[str]=[]


                #return a list of present student
                if type(seance_data.image) ==list :
                    for img in seance_data.image:
                        for ele in utils.recognize_faces_present_seance(seance_data,img):
                            present_student.append(ele)
                else :
                    for ele in utils.recognize_faces_present_seance(seance_data,seance_data.image):
                        present_student.append(ele)
                #students name are separated by underscores in the db and the encodings
                students_class=data_base_getters.get_class_students(class_obj.pk)
                

                ###########seance init
                seance_init=data_base_setters.set_seance_data(class_obj.pk ,module_obj.pk ,seance_data.created_at )
                
                present_student_obj=[]
                absence_student_obj=[]    
                
                ######## getting the modules of class




                #########setting the absence and presence of students
                for student in students_class :
                    if student.student_name in present_student :
                        present_student_obj.append(student)
                        data_base_setters.set_student_state(
                            student_id =student.pk,
                            seance_id=seance_init.pk,
                            state= True, 
                        ) 
                    else :
                        absence_student_obj.append(student)
                        # absence_student.append(' '.join(student.student_name.split('_')))
                        data_base_setters.set_student_state(
                            student_id =student.pk,
                            seance_id=seance_init.pk,
                            state= False, 
                        )  
                form = SeanceData()
                json_object={
                    'form': form,
                    'response_data':False,
                    'module_name':module_obj.module_name,
                    'seance_id':seance_init.seance_id,
                    'teacher':module_obj.teacher.teacher_name,
                    'present_student':present_student_obj,
                    'absent_student':absence_student_obj,
                    'start_hour':seance_init.start_hour,
                    'end_hour':seance_init.end_hour,
                }
                # Redirect to a new URL after successful form submission
                return render(request ,'face_recognizer.html',json_object)
                # return JsonResponse(json_object)
            except Exception as e :
                stri = str(e)
                print('en error occured :' ,stri)
                return HttpResponseServerError(f'the server cannot respond now internal server error has occured {stri}')
                # return JsonResponse({'en error occured ' :stri},status=500)
    return render(request, 'face_recognizer.html', {'form': form, 'response_data':False})

def result_submission(request):
    pass
def updateStatus(request: HttpRequest) -> HttpResponse:
    if request.method == 'PUT':
        try:
            data = loads(request.body)
            for ele in data :
                print(ele)
                student_id = ele['studentId']
                seance_id = ele['seanceId']
                presence_status = ele['presenceStatus']
                data_base_setters.update_student_state(student_id,seance_id,presence_status)
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
def student_info(request , student_id):
    return render(request, 'student_info.html')
