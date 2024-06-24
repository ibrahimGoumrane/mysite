from datetime import datetime, timedelta,date
import math
from pathlib import Path
from .forms import SeanceData
from .models import UtilsData 
from .detector import face_handler 
class Utils :
    def set_current_time(self,date:datetime=datetime.now())->dict:
        Date_Info =  date.strftime("%Y-%m-%d")
        current_day = date.strftime('%A')
        current_hour = math.floor(date.hour)
        return {
            'start_hour': current_hour,
            'end_hour': current_hour + 2,
            'week_day': current_day,
            'full_date': Date_Info,
        }
    def upload_location(self ,instance, filename:str)->str:
            cycle = instance.cycle.lower()
            file_location=f'uploads/{cycle}/'
            if cycle == 'ci':
                filiere = instance.filiere.lower()
                year = instance.cycle_eng  
                return file_location+f'{year}/{filiere}/{filename}'
            year=instance.cycle_prepa
            section =instance.section.lower()
            return file_location +f'{year}/{section}/{filename}'   
    def recognize_faces_present_seance(self,seance_data:UtilsData,image)->list:
            extension =str(image).split('.')[-1]
            if extension.find('png')==-1 and extension.find('jpeg')!=-1 and extension.find('jpg')!=-1 :
                 raise Exception('extension de image entrer n\'est pas correct.')
            img_path=Path('media').joinpath(Path(str(image)))
            cycle = ''
            year = ''
            section_filiere = ''
            img = img_path.absolute()
            if seance_data.cycle == 'cycle_preparatoire':
                cycle = 'cp'
                year=seance_data.cycle_prepa
                section_filiere = seance_data.section 
            else :
                cycle = 'ci'
                year=seance_data.cycle_eng
                section_filiere = seance_data.filiere        
            #it should be async where i need to display like an animation
            return face_handler.recognize_faces(cycle,year,section_filiere,img)
    def utilsdata_init(self,module:str,form:SeanceData)->UtilsData:
        module_name = module
        cycle = form.cleaned_data['cycle']
        cycle_prepa = form.cleaned_data['cycle_prepa'] 
        cycle_eng =form.cleaned_data['cycle_eng']
        filiere = form.cleaned_data['filiere']
        image = form.cleaned_data['image']
        section = form.cleaned_data['section']
        # Create an instance of the Seance model
        return UtilsData.objects.create(
        module_name=module_name,
        cycle=cycle,
        cycle_eng=cycle_eng,
        cycle_prepa=cycle_prepa,
        filiere=filiere,
        image=image,
        section=section,
        )
utils=Utils()
