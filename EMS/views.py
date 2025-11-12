
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Count
from django.contrib import messages
from .models import Student, Department,Subjects,StudentRequest,CarouselImage,Card,Semester,Result


# send data to home.html
def home(request):
    craousel_img = CarouselImage.objects.all()
    card = Card.objects.all()
    context ={
        'craousel_img':craousel_img,
        'card':card
    }
    return render(request, 'home.html',context)

# create API for chart 
def chart_data(request):
    data = Student.objects.values('department__departmentName').annotate(total=Count('id'))
    return JsonResponse(list(data), safe=False)

  
 # register views 
def register(request):
   departments = Department.objects.all()  
   if request.method == 'POST':
        # Text fields
        student_bangla_name = request.POST.get('bangla_name')
        student_name = request.POST.get('english_name')
        student_phone_number = request.POST.get('phone_num')
        fathers_name = request.POST.get('fathers_name')
        fathers_phone_number = request.POST.get('fathers_phone_num')
        mothers_name = request.POST.get('mothers_name')
        mothers_phone_number = request.POST.get('mothers_phone_num')
        address = request.POST.get('address')
        post_code = request.POST.get('post_code')
        post_office = request.POST.get('post_off')
        word = request.POST.get('word_no')
        thana = request.POST.get('thana')
        district = request.POST.get('dist')
        nationality = request.POST.get('nationality')
        religion = request.POST.get('religion')
        examination = request.POST.get('exam')
        group = request.POST.get('group')
        board = request.POST.get('board')
        department_name = request.POST.get('department')
        regi_no = request.POST.get('reg_no')
        gpa = request.POST.get('gpa')
        exam_year = request.POST.get('exam_year')
        
        department=departments.get(departmentName=department_name)
        # File upload
        student_photo = request.FILES.get('profile_pic')
        date_of_birth = request.POST.get('birth_date')
        
        Student_request =StudentRequest(
            student_bangla_name=student_bangla_name,
            student_name=student_name,
            student_phone_number=student_phone_number,
            fathers_name=fathers_name,
            fathers_phone_number=fathers_phone_number,
            mothers_name=mothers_name,
            mothers_phone_number=mothers_phone_number,
            address=address,
            post_office=post_office,
            word=word,
            post_code=post_code,
            thana=thana,
            district=district,
            nationality=nationality,
            date_of_birth=date_of_birth,
            religion=religion,
            examination=examination,
            group=group,
            regi_no=regi_no,
            board=board,
            exam_year=exam_year,
            gpa=gpa,
            department=department,
            student_photo=student_photo, 
            )
        Student_request.save()
        messages.success(request, "Register Successful!")
        
        # Create cookie
        response = redirect(f'/request_status/{regi_no}')
        response.set_cookie('last_registered', student_name, max_age=7*24*60*60)  
        # max_age = 7 days        
        return response
   else:
        return render(request, "register.html", {'department': departments})


# for login page 
def login(request):
    # get deparment data from Deparment table
    department = Department.objects.all()

    if request.method == 'POST':
        registation_no = request.POST.get('registation_no')
        department_name = request.POST.get('department')

        try:
            # find  Student and Department 
            student = Student.objects.get(HonorsRegisterNO=registation_no)
            department_obj = Department.objects.get(departmentName=department_name)

            # verify student is that department 
            if Student.objects.filter(department_id=department_obj.id, HonorsRegisterNO=student.HonorsRegisterNO).exists():
                # SESSION set
                request.session['student_id'] = student.id
                request.session['student_name'] = student.student_name
                request.session['department'] = department_obj.departmentName
                request.session.set_expiry(3600)  # 1 huor will stay

                # COOKIE set
                response = redirect(f'/profile/{student.id}')
                messages.success(request, "Login successful!")
                response.set_cookie('last_login_user', student.student_name, max_age=7*24*60*60)  # 7 day will stay
                return response

            else:
                messages.error(request, "Invalid Registration No or Department!")
                return redirect('/')
        
        except Student.DoesNotExist:
            return redirect('/')
        
        except Department.DoesNotExist:
            return redirect('/')

    else:
        return render(request, 'login.html', {'department': department})


#show student data
def result(request,id):

  student_id = Student.objects.get(id=id)
  dept_id = student_id.department_id
  department = Department.objects.get(id=dept_id)
  subjects = Subjects.objects.filter(department_id = dept_id)
  semesters = Semester.objects.all().order_by('semester_number')
  total_cgpa = student_id.total_cgpa
  print(total_cgpa)
  context = {
    'department':department,
    'member':student_id,
    'subjects':subjects,
    'semesters':semesters,
    'total_cgpa':total_cgpa
    }
  return render(request, 'result.html',context)


def get_student_results(request):
    student_id = request.GET.get('student_id')
    semester_id = request.GET.get('semester_id')
    
    results_list = []
    if student_id and semester_id:
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

        results = Result.objects.filter(student_id=student_id, semester_id=semester_id)
        for r in results:           
            results_list.append({
                'subject': r.subject.subject,
                'code': r.subject.subjectCode,
                'exam': r.exam_type,
                'marks': r.marks,
                'grade': r.grade,
                'cgpa': r.cgpa,
            })
        return JsonResponse({'results': results_list})
    else:
        return JsonResponse({'error': 'Missing student_id or semester_id'}, status=400)
     

# stduent request handel
def request_status(request, regi_no):

    try:
        student_request = StudentRequest.objects.get(regi_no=regi_no)
        context = {'requests': student_request}
        return render(request, 'request_status.html', context)

    except StudentRequest.DoesNotExist:
        try:
            student = Student.objects.get(regi_no=regi_no)
            context = {'student': student}
            return render(request, 'request_status.html', context)
        except Student.DoesNotExist:
            return HttpResponse("<h3>No request or approved student found.</h3>")



def student_dashboard():
  pass


# student profile handel
def profile(request,id): 
  student_id = Student.objects.get(id=id)
  return render(request,'profile.html',{'student':student_id})
  
  

def admin_dashboard():
  pass

def admin_student_detail():
  pass


# student approve request handel 
def approve_request(request, req_id):
    req = get_object_or_404(StudentRequest, id=req_id)
    req.status = 'approved'
    req.save()

    student = Student(
        student_bangla_name=req.student_bangla_name,
        student_name=req.student_name,
        student_phone_number=req.student_phone_number,
        fathers_name=req.fathers_name,
        fathers_phone_number=req.fathers_phone_number,
        mothers_name=req.mothers_name,
        mothers_phone_number=req.mothers_phone_number,
        address=req.address,
        post_office=req.post_office,
        word=req.word,
        post_code=req.post_code,
        thana=req.thana,
        district=req.district,
        nationality=req.nationality,
        date_of_birth=req.date_of_birth,
        religion=req.religion,
        examination=req.examination,
        group=req.group,
        regi_no=req.regi_no,
        board=req.board,
        exam_year=req.exam_year,
        gpa=req.gpa,
        department=req.department,
        student_photo=req.student_photo,
        roll=req.roll,
    )
    student.save()
    return redirect('pending_requests')


def Edit(request,id):
    edit_student = Student.objects.get(id=id)
    return render(request,'edit.html',{'edit_student':edit_student})
  

#for logout student
def logout(request):
    request.session.flush()  # session data delete
    response = redirect('/')
    response.delete_cookie('last_login_user')
    return response

  