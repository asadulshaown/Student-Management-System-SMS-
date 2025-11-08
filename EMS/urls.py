
from django.urls import path
from . import views
from django.contrib.auth.models import User


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/',views.login,name='login'),
    path('chart_data/', views.chart_data, name='chart_data'),
 
    # Student URLs
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('request_status/<int:regi_no>/',views.request_status,name='request_status'),
    path('result/<int:id>/',views.result, name='result'),
    path('logout/',views.logout,name='logout'),
    path('edit/<int:id>/', views.Edit,name='edit'),
    path('get_student_results/', views.get_student_results, name='get_student_results'),
    
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/student/<int:student_id>/', views.admin_student_detail, name='admin_student_detail'),
]
