
from django.contrib import admin
from django.urls import path,reverse
from django.shortcuts import redirect,render
from django.contrib import messages
from django.utils.html import format_html
from .forms import ApproveStudentForm
from .models import Student,Department,Subjects,StudentRequest,CarouselImage

admin.site.register(Department)
admin.site.register(Subjects)
admin.site.register(CarouselImage)

admin.site.site_header="Student Admin Panel"
admin.site.index_title = "Admin Dashboard"

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # admin only acn see this
       readonly_fields = [
        'student_name',
        'student_phone_number',
        'fathers_name',
        'fathers_phone_number',
        'mothers_name',
    ]
    
    # admin only edit this field   
       fields = [
        'HonorsRegisterNO',
        'roll'
        
    ]
       list_display =[
        'student_name',
        'student_phone_number',
        'department',
        'roll',
        'HonorsRegisterNO'
       ]
    
    

@admin.register(StudentRequest)
class StudentRequestAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'department','examination','group','exam_year','gpa','roll','HonorsRegisterNO', 'approve_button','reject_button')
    
    fields = [
        'student_name', 
        'examination',
        'group',
        'exam_year',
        'gpa',
    ]
    
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:request_id>/approve/',
                self.admin_site.admin_view(self.approve_request),
                name='EMS_studentrequest_approve'
            ),
            path(
                '<int:request_id>/reject/',
                self.admin_site.admin_view(self.reject_request),
                name='EMS_studentrequest_reject'
            ),
        ]
        return custom_urls + urls

    # Approve Button
    def approve_button(self, obj):
        url = reverse('admin:EMS_studentrequest_approve', args=[obj.id])
        return format_html('<a class="btn btn-success" href="{}">Approve</a>', url)
    approve_button.short_description = 'Approve'

    # Reject Button
    def reject_button(self, obj):
        url = reverse('admin:EMS_studentrequest_reject', args=[obj.id])
        return format_html('<a class="btn btn-danger" href="{}">Reject</a>', url)
    reject_button.short_description = 'Reject'

    # Approve View
    def approve_request(self, request, request_id):
      student_request = self.get_object(request, request_id)
    
      if not student_request:
        messages.error(request, "Request not found")
        return redirect('/admin/EMS/studentrequest/')

      if request.method == "POST":
        form = ApproveStudentForm(request.POST, instance=student_request)
        if form.is_valid():
            # roll update
            student_request = form.save(commit=False)
            student_request.status = "Approved"
            student_request.save()

            # save into Student model
            student = Student(
                student_bangla_name=student_request.student_bangla_name,
                student_name=student_request.student_name,
                student_phone_number=student_request.student_phone_number,
                fathers_name=student_request.fathers_name,
                fathers_phone_number=student_request.fathers_phone_number,
                mothers_name=student_request.mothers_name,
                mothers_phone_number=student_request.mothers_phone_number,
                address=student_request.address,
                post_office=student_request.post_office,
                word=student_request.word,
                post_code=student_request.post_code,
                thana=student_request.thana,
                district=student_request.district,
                nationality=student_request.nationality,
                date_of_birth=student_request.date_of_birth,
                religion=student_request.religion,
                examination=student_request.examination,
                group=student_request.group,
                regi_no=student_request.regi_no,
                board=student_request.board,
                exam_year=student_request.exam_year,
                gpa=student_request.gpa,
                department=student_request.department,
                student_photo=student_request.student_photo,
                roll=student_request.roll,
                HonorsRegisterNO = student_request.HonorsRegisterNO
            )
            student.save()
            # StudentRequest delete
            student_request.delete()
            
            messages.success(request, f"{student_request.student_name} has been approved Roll: {student_request.roll}")
            return redirect('/admin/EMS/studentrequest/')
             
      else:
        # set ApproveStudentForm for form
        form = ApproveStudentForm(instance=student_request)

      context = {
        "form": form,
        "student_request": student_request,
        "title": f"Approve Student: {student_request.student_name}",
      }
      return render(request, "admin/approve_student_form.html", context)


    # Reject View
    def reject_request(self, request, request_id):
        student_request = self.get_object(request, request_id)
        if student_request:
            student_request.status = "Rejected"
            student_request.delete()
            messages.error(request, f"{student_request.student_name} has been rejected ")
        else:
            messages.error(request, "Request not found ")
        return redirect('/admin/EMS/studentrequest/')