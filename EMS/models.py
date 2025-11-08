
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver



# Department Table
class Department(models.Model):
    departmentName = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.departmentName

    class Meta:
        verbose_name_plural = "Departments"
 
            
# Semester model
class Semester(models.Model):
    semester_name = models.CharField(max_length=50, null=True, blank=True)  
    semester_number = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.semester_name


# Subject Table
class Subjects(models.Model):
    subject = models.CharField(max_length=100,null=True,blank=True)
    subjectCode = models.CharField(max_length=20, null=True, blank=True, default="0")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="subjects", null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE , null=True, blank=True)

    def __str__(self):
        return f"{self.subject} ({self.subjectCode}) {self.semester.semester_name}"

    class Meta:
        verbose_name_plural = "Subjects"


# create Student table
class Student(models.Model):
    student_bangla_name = models.CharField(max_length=50, null=True, blank=True)
    student_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField( null=True, blank=True)
    student_phone_number = models.CharField(max_length=15, null=True, blank=True)
    fathers_name = models.CharField(max_length=50, null=True, blank=True)
    fathers_phone_number = models.CharField(max_length=15, null=True, blank=True)
    mothers_name = models.CharField(max_length=50, null=True, blank=True)
    mothers_phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    post_office = models.CharField(max_length=50, null=True, blank=True)
    word = models.CharField(max_length=30, null=True, blank=True)
    post_code = models.CharField(max_length=10, null=True, blank=True)
    thana = models.CharField(max_length=30, null=True, blank=True)
    district = models.CharField(max_length=30, null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    religion = models.CharField(max_length=30, null=True, blank=True)
    examination = models.CharField(max_length=30, null=True, blank=True)
    group = models.CharField(max_length=30, null=True, blank=True)
    regi_no = models.CharField(max_length=20, null=True, blank=True)
    board = models.CharField(max_length=30, null=True, blank=True)
    exam_year = models.CharField(max_length=10, null=True, blank=True)
    gpa = models.CharField(max_length=10, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="students")
    session = models.CharField(max_length=20, null=True, blank=True)
    student_photo = models.ImageField(upload_to='images/student_photo/', default="images/student_photo/server4.webp", null=True, blank=True)
    roll = models.IntegerField(default=0, null=True, blank=True)
    HonorsRegisterNO = models.IntegerField( default=0,null=True,blank=True)
    approved_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.student_name} ({self.department.departmentName})"

    class Meta:
        verbose_name_plural = "Students"



# create Student Request table
class StudentRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    student_bangla_name = models.CharField(max_length=50, null=True, blank=True)
    student_name = models.CharField(max_length=50, null=True, blank=True)
    student_phone_number = models.CharField(max_length=15, null=True, blank=True)
    fathers_name = models.CharField(max_length=50, null=True, blank=True)
    fathers_phone_number = models.CharField(max_length=15, null=True, blank=True)
    mothers_name = models.CharField(max_length=50, null=True, blank=True)
    mothers_phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    post_office = models.CharField(max_length=50, null=True, blank=True)
    word = models.CharField(max_length=30, null=True, blank=True)
    post_code = models.CharField(max_length=10, null=True, blank=True)
    thana = models.CharField(max_length=30, null=True, blank=True)
    district = models.CharField(max_length=30, null=True, blank=True)
    nationality = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    religion = models.CharField(max_length=30, null=True, blank=True)
    examination = models.CharField(max_length=30, null=True, blank=True)
    group = models.CharField(max_length=30, null=True, blank=True)
    regi_no = models.CharField(max_length=20, null=True, blank=True)
    board = models.CharField(max_length=30, null=True, blank=True)
    exam_year = models.CharField(max_length=10, null=True, blank=True)
    gpa = models.CharField(max_length=10, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    student_photo = models.ImageField(upload_to='images/student_photo/', null=True, blank=True)
    roll = models.IntegerField(default=0, null=True, blank=True)
    HonorsRegisterNO = models.IntegerField(default=0, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.student_name} - {self.status}"

    class Meta:
        verbose_name_plural = "Student Requests"


# Marks / Result Model
class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, null=True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True)
    exam_type = models.CharField(
        max_length=50,
        choices=[
            ('Midterm', 'Midterm'),
            ('Final', 'Final'),
            ('Improvement', 'Improvement'),
        ],
        default='Final'
    )
    marks = models.FloatField(null=True, blank=True)
    grade = models.CharField(max_length=2,null=True, blank=True)
    cgpa = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return f"{self.student.student_name} - {self.subject.subject} ({self.exam_type}) {self.semester.semester_name}"

    # Function to calculate grade and GPA automatically
    def save(self, *args, **kwargs):
        if self.marks >= 80:
            self.grade = 'A+'
            self.cgpa = 4.00
        elif self.marks >= 70:
            self.grade = 'A'
            self.cgpa = 3.50
        elif self.marks >= 60:
            self.grade = 'A-'
            self.cgpa = 3.00
        elif self.marks >= 50:
            self.grade = 'B'
            self.cgpa = 2.50
        elif self.marks >= 40:
            self.grade = 'C'
            self.cgpa = 2.00
        elif self.marks >= 33:
            self.grade = 'D'
            self.cgpa = 1.00
        else:
            self.grade = 'F'
            self.cgpa = 0.00
        super().save(*args, **kwargs)
     

# create CarouselImage table
class CarouselImage(models.Model):
    carousel_images = models.ImageField(upload_to='images/carousel_images/',default="images/carousel_images/sis.png", null=True, blank=True)
    carousel_image_name = models.CharField(max_length=100, null=True,blank=True)
    
    def __str__(self):
        return f"{self.carousel_image_name}"

    class Meta:
        verbose_name_plural = "Carousel Images"


# create Card table
class Card(models.Model):
    card_name = models.CharField(max_length=100,null=True,blank=True)
    card_image = models.ImageField(upload_to='images/card_images/', null=True, blank=True)
    card_description = models.CharField(max_length=200,null=True,blank=True)
    
    def __str__(self):
        return f"{self.card_name}"
    
