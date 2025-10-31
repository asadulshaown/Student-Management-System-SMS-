
from django.db import models
from django.utils import timezone


# ==========================
# Department Table
# ==========================
class Department(models.Model):
    departmentName = models.CharField(max_length=50)

    def __str__(self):
        return self.departmentName

    class Meta:
        verbose_name_plural = "Departments"
            


# ==========================
# Subject Table
# ==========================
class Subjects(models.Model):
    subject = models.CharField(max_length=100)
    subjectCode = models.CharField(max_length=20, default="0")  # Changed to CharField
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="subjects")

    def __str__(self):
        return f"{self.subject} ({self.subjectCode})"

    class Meta:
        verbose_name_plural = "Subjects"


# ==========================
# Approved Student Model
# ==========================
class Student(models.Model):
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
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="students")
    student_photo = models.ImageField(upload_to='images/student_photo/', default="images/students_photo/profile.png", null=True, blank=True)
    roll = models.IntegerField(default=0, null=True, blank=True)
    HonorsRegisterNO = models.IntegerField( default=0,null=True,blank=True)
    approved_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return f"{self.student_name} ({self.department.departmentName})"

    class Meta:
        verbose_name_plural = "Students"


# ==========================
# Pending Student Request Model
# ==========================
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
        

class CarouselImage(models.Model):
    carousel_images = models.ImageField(upload_to='images/carousel_images/',default="images/carousel_images/sis.png", null=True, blank=True)
    carousel_image_name = models.CharField(max_length=100, null=True,blank=True)
    
    def __str__(self):
        return f"{self.carousel_image_name}"

    class Meta:
        verbose_name_plural = "Carousel Image"
