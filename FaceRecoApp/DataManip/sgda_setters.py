from FaceRecoApp.models import Class, Teachers, Students, Module, Seance, Presence
from datetime import datetime
from FaceRecoApp.DetectorMain.utils import utils

class DataBaseSetters:
    #  if you want to create a new Students object and associate it with a Class object 
    #  using the foreign key relationship, you would typically pass the Class object
    #  itself rather than just its ID. 
    def set_student_data(self, student_name: str, class_id: int) -> None:
        try:
            student_class = Class.objects.get(pk=class_id)
            Students.objects.create(student_name=student_name, student_class=student_class)
            print("Student data inserted successfully.")
        except Exception as e:
            print(f"An error occurred during student {student_name} initialization: {e}")

    def set_teacher_data(self, teacher_name: str) -> None:
        try:
            Teachers.objects.create(teacher_name=teacher_name)
            print("Teacher data inserted successfully.")
        except Exception as e:
            print(f"An error occurred during teacher {teacher_name} initialization: {e}")

    def set_class_data(self, cycle: str, cycle_year: int, filiere: str) -> None:
        try:
            Class.objects.create(cycle=cycle, cycle_year=cycle_year, filiere=filiere)
            print("Class data inserted successfully.")
        except Exception as e:
            print(f"An error occurred during class initialization: {e}")

    def set_seance_data(self, class_id: int, module_id: int, date: datetime = datetime.now()) -> Seance:
        Date_info=utils.set_current_time(date)
        try:
            seance_class = Class.objects.get(pk=class_id)
            module = Module.objects.get(pk=module_id)
            newSeance =Seance(
                student_class=seance_class,
                module=module,
                start_hour=Date_info['start_hour'],
                end_hour=Date_info['end_hour'] ,  # Assuming each session lasts for 2 hour
                week_day=Date_info["week_day"],
                full_date=Date_info['full_date'],
            )
            newSeance.save()
            print("Seance data inserted successfully.")
            return newSeance
        except Exception as e:
            print(f"An error occurred during seance initialization: {e}")

    def set_module_data(self, class_id: int, module_name: str, teacher_id: int) -> None:
        try:
            class_object = Class.objects.get(pk=class_id)
            teacher = Teachers.objects.get(pk=teacher_id)
            Module.objects.create(student_class=class_object, module_name=module_name, teacher=teacher)
            print("Module data inserted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
    def update_student_state(self ,student_id:int,seance_id:int,new_state:str):
        try:
            student_obj = Presence.objects.filter(seance__seance_id=seance_id,student__student_id=student_id)
            if new_state=='Present':
                student_obj.update(state=True)
            else:
                student_obj.update(state=False)
            print("Student state updated successfully.")
        except Presence.DoesNotExist as e :
            print("Presence doesn't exist ")    
        except Exception as e:
            print(f"An error occurred: {e}")
    def set_student_state(self, student_id: int, seance_id: int, state: bool = False) -> None:
        try:
            student = Students.objects.get(pk=student_id)
            seance = Seance.objects.get(pk=seance_id)
            Presence.objects.create(student=student, seance=seance, state=state)
            print("Student state inserted successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")

data_base_setters =DataBaseSetters()