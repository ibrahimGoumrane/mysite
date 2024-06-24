from django.test import TestCase
# Create your tests here.

from datetime import datetime
from FaceRecoApp.models import Class, Students, Seance, Presence
from FaceRecoApp.utils import utils
from FaceRecoApp.sgda_getters import Data_Base_extracters

class_instance = Class.objects.create(cycle="Test Cycle", cycle_year=2024, filiere="Test Filiere")
student_instance = Students.objects.create(student_name="Test Student", student_class=class_instance)


date_now = datetime.now()
seance_instance = Seance.objects.create(student_class=class_instance, module=None,
                                        start_hour=date_now.hour, end_hour=date_now.hour + 2,
                                        week_day=date_now.strftime("%A"), full_date=date_now.strftime("%Y-%m-%d"))


Presence.objects.create(seance=seance_instance, student=student_instance, state=False)


db_extracters = Data_Base_extracters()

# Testing get_students_class function
student_class_id = db_extracters.get_students_class(student_instance.pk)
print("Student's class ID:", student_class_id)

# Testing get_seance function
seance_id = db_extracters.get_seance(class_instance.pk, date_now)
print("Seance ID:", seance_id)

# Testing get_class_absence_list function
absence_list = db_extracters.get_class_absence_list(class_instance.pk, date_now)
print("Class absence list:", absence_list)

# Testing get_seance_date function
seance_date = db_extracters.get_seance_date(class_instance.pk, date_now)
print("Seance date:", seance_date)

# Testing get_student_absence_seance_based function
student_absence_seance_based = db_extracters.get_student_absence_seance_based(student_instance.pk, date_now)
print("Student absence (seance based):", student_absence_seance_based)

# Testing get_student_absence_module_based function
student_absence_module_based = db_extracters.get_student_absence_module_based(student_instance.pk, None)
print("Student absence (module based):", student_absence_module_based)
