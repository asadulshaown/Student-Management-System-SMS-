
from django.contrib import admin
from django.urls import path,reverse
from django.shortcuts import redirect,render
from django.contrib import messages
from django.utils.html import format_html
from .forms import ApproveStudentForm
from django.http import JsonResponse
from .models import Student,Department,Subjects,StudentRequest,CarouselImage,Card,Result,Semester

admin.site.site_header="Student Admin Panel"
admin.site.index_title = "Admin Dashboard"


# register Subject model 
@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('subject','subjectCode')
    


admin.site.register(Semester)


# register Result model
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display =('student','subject','exam_type','marks','grade')
    
    fields = [
        'student',
        'semester',
        'subject',
        'exam_type',
        'marks'
        
    ]
    
    # Dynamic filtering: Only show subjects of selected semester
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            if request._obj_ is not None:
                kwargs["queryset"] = Subjects.objects.filter(semester=request._obj_.semester_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    # Store the object in request for dynamic filtering
    def get_form(self, request, obj=None, **kwargs):
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)

# register Department table from model
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['departmentName',]
    change_list_template = "admin/department_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "filter-students/",
                self.admin_site.admin_view(self.filter_students),
                name="filter_students",
            ),
        ]
        return custom_urls + urls

    def filter_students(self, request):
        dept_id = request.GET.get("dept_id")
        students = list(
            Student.objects.filter(department_id=dept_id)
            .values('student_name','roll','district','student_phone_number')
        )
        return JsonResponse(students, safe=False)

    class Media:
         css = {'all': ('css/admin_custom.css',)}
         js = ('javascript/department_filter.js')


# register Student table form database
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):    
    # admin only edit this field   
       fields = [
        'HonorsRegisterNO',
        'roll',
        'student_photo'      
    ]
       list_display =(
        'student_name',
        'student_phone_number',
        'fathers_name',
        'department',
        'roll',
        'HonorsRegisterNO'
       )
    
       
    
    
# register StudentRequest table from model
@admin.register(StudentRequest)
class StudentRequestAdmin(admin.ModelAdmin):
    list_display = ('student_name','student_phone_number','fathers_name', 'department','examination','group','exam_year','gpa','district','approve_button','reject_button')
    
    # admin can edit this field
    fields = [
        'submitted_at', 
    ]
    
    # make url for approve and reject button in admin dasboard 
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:request_id>/approve/',self.admin_site.admin_view(self.approve_request),name='EMS_studentrequest_approve'),
            
            path('<int:request_id>/reject/',self.admin_site.admin_view(self.reject_request),name='EMS_studentrequest_reject'),
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
            # student approve by admin
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
            # student delete from StudentRequest table
            student_request.delete()
            
            messages.success(request, f"{student_request.student_name} has been approved Roll: {student_request.roll}")
            return redirect('/admin/EMS/studentrequest/')
             
      else:
        # set ApproveStudentForm for form
        form = ApproveStudentForm(instance=student_request)

        # send data to admin/approve_student_form.html
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


# register CarouselImage from model
@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    # admin show this list_display element
    list_display = ('carousel_image_name','image_preview')

    def image_preview(self, obj):
        if obj.carousel_images:
            return format_html(
                '<img src="{}" />',
                obj.carousel_images.url
            )
        return "No Image" 
    # import css file for design admin panel
    class Media:
        css = {'all': ('css/admin_custom.css',)}


# register card from card table
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    # admin show this list_display element
    list_display = ('card_name','short_description','image_preview')

    def image_preview(self, obj):
        if obj.card_image:
            return format_html(
                '<img src="{}" />',
                obj.card_image.url
            )
        return "No Image"
    image_preview.short_description = 'Preview'

    def short_description(self, obj):
        if obj.card_description:
            return obj.card_description[:40] + ("..." if len(obj.card_description) > 40 else "")
        return ""
    short_description.short_description = 'Description'
    # import css file for design admin panel
    class Media:
        css = {'all': ('css/admin_custom.css',)}