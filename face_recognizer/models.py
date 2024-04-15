from typing import Any
from django.db import models

# Create your models here.
#so in django the api that controls data flow over db auto convert the name of the models to lowercase
#in case we wanna access A realted obj from another one for example 
'''
q = Question.objects.get(pk=1)
q.choice_set.all() to get  all Choice related objects to question with pk=1
q.choice_set.create(choice_text="Not much", votes=0) to associate
a specific Question  object with a new choice
'''
#Choice.objects.all() to get all instance (table rows ) of the Choice class
#Choice.objects.filter(votes__gt=50) filter by field name and condition
#Choice.objects.get(condition)  return only one result. pk mean  primary key.
#Choice.objects.filter(question__pub_date__year=current_year) __to separate relationships.
#Question.objects.filter(pub_date__year=timezone.now().year)


class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    cycle = models.TextField()
    cycle_year = models.IntegerField()
    filiere = models.TextField()

    class Meta:
        db_table = 'class'

    def __str__(self):
        return f'Class ID: {self.class_id}, Cycle: {self.cycle}, Year: {self.cycle_year}, Filiere: {self.filiere}'

class Teachers(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    teacher_name = models.TextField()

    class Meta:
        db_table = 'teachers'

    def __str__(self):
        return f'Teacher ID: {self.teacher_id}, Name: {self.teacher_name}'


class Students(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.TextField()
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id', null=True ,related_name ='class_students')

    class Meta:
        db_table = 'students'

    def __str__(self):
        return f'Student ID: {self.student_id}, Name: {self.student_name}, Class ID: {self.student_class_id}'


class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    student_class = models.ManyToManyField(Class, db_column='class_id',related_name='module_class')
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE, db_column='teacher_id', null=True)
    module_name = models.TextField(null=False)

    class Meta:
        db_table = 'module'

    def __str__(self):
        first_class : Class = self.student_class.first() 
        return f'Module ID: {self.module_id}, Cycle: {first_class.cycle}, Cycle_year: {first_class.cycle_year}, Teacher ID: {self.teacher_id}, Name: {self.module_name}'
    def delete(self, *args, **kwargs):
        # Clear all related students before deleting the course
        self.student_class.clear()
        super(Module,self).delete(*args, **kwargs)

class Seance(models.Model):
    seance_id = models.AutoField(primary_key=True)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id', null=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, db_column='module_id', null=True)
    start_hour = models.IntegerField()
    end_hour = models.IntegerField()
    week_day = models.CharField(max_length=10)
    full_date = models.DateField()

    class Meta:
        db_table = 'seance'

    def __str__(self):
        return f'Seance ID: {self.seance_id}, Class ID: {self.student_class.class_id}, Module ID: {self.module_id}, Start Hour: {self.start_hour}, End Hour: {self.end_hour}, Week Day: {self.week_day}, Full Date: {self.full_date}'


class Presence(models.Model):
    presence_id = models.AutoField(primary_key=True)
    seance = models.ForeignKey(Seance, on_delete=models.CASCADE, db_column='seance_id', default=None)
    student = models.ForeignKey(Students, on_delete=models.CASCADE, db_column='student_id')
    state = models.BooleanField(default=False)  # Renamed to use False instead of 0 for clarity

    class Meta:
        db_table = 'presences'

    def __str__(self):
        return f'Presence ID: {self.presence_id}, Seance ID: {self.seance_id}, Student ID: {self.student_id}, State: {self.state}'


class Contact(models.Model):
    name = models.CharField(db_column="name", max_length=256, null=True)
    firstName = models.CharField(db_column="firstName", max_length=256, null=True)
    email = models.EmailField(max_length=150)
    subject = models.TextField()
    description = models.TextField()

    class Meta:
        db_table = 'contact'

    def __str__(self):
        return f'Name: {self.name}, Email: {self.email}, Subject: {self.subject}'

class FaceRecognizer(models.Model):
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE, db_column='class_id', null=True)
    binary_steam = models.BinaryField()
    class Meta:
        db_table = 'face_recognizer'
    def __str__(self):
        return f'Student Class: {self.student_class}'


# Define upload_location function here

# Define choices for the 'cycle' field
cycle = [
    (None, ''),
    ('cycle_preparatoire', 'Preparatory Cycle'),
    ('cycle_ingenieur', 'Engineering Cycle'),
]

# Define choices for the 'cycle_year' field
cycle_year = {
    'prep_years': [
        (None, ''),
        ('1', '1 year'),
        ('2', '2 years'),
    ],
    'engineer_years': [
        (None, ''),
        ('1', '1 year'),
        ('2', '2 years'),
        ('3', '3 years'),
    ]
}

# Define choices for the 'filiere' field
filiere = [
    (None, ''),
    ('GM', 'Genie Mecanique'),
    ('GEM', 'Genie Electromecanique'),
    ('IAGI', 'Genie Informatique'),
    ('GI', 'Genie Industrielle'),
    ('MSEI', 'Genie Electrique'),
]

# Define choices for the 'section' field
section = [
    (None, ''),
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
]

def upload_location(instance, filename:str)->str:
        cycle = instance.cycle.lower()
        file_location=f'uploads/{cycle}/'
        if cycle == 'cycle_ingenieur':
            filiere = instance.filiere.lower()
            year = instance.cycle_eng  
            return file_location+f'{year}/{filiere}/{filename}'
        year=instance.cycle_prepa
        section =instance.section.lower()
        return file_location +f'{year}/{section}/{filename}'
class UtilsData(models.Model):
    module_name = models.CharField(max_length=400 ,db_column='module')
    cycle = models.CharField(max_length=80, choices=cycle ,db_column='cycle') 
    cycle_prepa = models.CharField(max_length=80, choices=cycle_year['prep_years'], blank=True, null=True ,db_column='cycle_prepa')
    cycle_eng = models.CharField(max_length=80, choices=cycle_year['engineer_years'], blank=True, null=True ,db_column='cycle_eng')
    filiere = models.CharField(max_length=80, choices=filiere , blank=True, null=True ,db_column='filiere')
    section = models.CharField(max_length=80, choices=section , blank=True, null=True ,db_column='section')
    image = models.FileField(upload_to=upload_location ,db_column='image_path') 
    created_at = models.DateTimeField(auto_now_add=True ,db_column='creation_date')
    class Meta:
        db_table = 'seancedata'
    def __str__(self):
        return f'''
        module_name: {self.module_name},
        cycle: {self.cycle}, 
        cycle_prepa: {self.cycle_prepa}, 
        cycle_eng: {self.cycle_eng},
        filiere: {self.filiere},
        section: {self.section},
        created_at: {self.created_at}'''
