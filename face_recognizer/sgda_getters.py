from datetime import datetime ,date
from face_recognizer.utils import utils
from face_recognizer.models import Class, Teachers, Students, Module, Seance, Presence
from typing import Dict, List

class Data_Base_extracters:
    def get_student_id(self,name:str) -> int :
        Student = Students.objects.get(student_name =name)
        return Student.pk
    def get_students_class(self, student_id: int) -> int:
        try:
        # Query the Students model to retrieve the student
            student = Students.objects.get(pk=student_id)

            # Access the student's class using the foreign key relationship
            student_class = student.student_class

            # Return the class ID of the student
            return student_class.class_id
        except Students.DoesNotExist:
            return None

    def get_seance(self, class_id: int, date: datetime = datetime.now()) -> int:
        Date_info = utils.set_current_time(date)
        try:
            seance = Seance.objects.get(student_class_id=class_id,
                                        start_hour=Date_info['start_hour'],
                                        end_hour=Date_info['end_hour'],
                                        week_day=Date_info['week_day'],
                                        full_date=Date_info['full_date'])
            return seance.seance_id
        except Seance.DoesNotExist:
            return None

    def get_class_absence_list(self, class_id: int, date: datetime = datetime.now()) -> List[Dict[str, any]]:
        seance_id = self.get_seance(class_id, date)
        try:
            # Use Django ORM to filter students and presence records based on class_id and seance_id
            # using orm you can do join easly
            absence_list = Presence.objects.filter(student__student_class_id=class_id, seance_id=seance_id)
            # Convert QuerySet to a list of dictionaries
            return absence_list
        except Presence.DoesNotExist:
            return []
    def get_seance_date(self, class_id: int, date: date) :
        Date_info = utils.set_current_time(date)
        return Seance.objects.filter(start_hour=Date_info['start_hour'],
                                            end_hour=Date_info['end_hour'],
                                            student_class_id=class_id)
    def get_student_absence_seance_based(self, student_id: int, date: date) ->dict:
        class_id = self.get_students_class(student_id)
        Date_info = utils.set_current_time(date)
        seances = self.get_seance_date(class_id,date)
        # values here is used to select the columns that we want to retrive
        student_absence_data = Presence.objects.filter(seance__in=seances, student_id=student_id).values('student__student_name', 'state')
        return {
            'name': student_absence_data[0]['student__student_name'] if student_absence_data else None,
            'sem': list(range(1, len(seances) + 1)),
            'start': Date_info['start_hour'],
            'end': Date_info['end_hour'],
            'state': [data['state'] for data in student_absence_data]
        }

    def get_student_absence_module_based(self, student_id: int, module_id: int) ->int :
        try :
            totalSeances = Presence.objects.filter(seance__module_id=module_id ,student_id =student_id).count()
            presences = Presence.objects.filter(seance__module_id=module_id ,student_id =student_id, state=True).count()
            presence_ratio = presences/totalSeances
            print('the student {} has an presence ratio of : {} %'.format(student_id,presence_ratio*100))
            return  presence_ratio *100 
        except Students.DoesNotExist:
            return None       
        except Class.DoesNotExist:
            return None