from django.urls import path
from . import views


app_name = 'supervisor'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('project/', views.project_view, name='project'),
    path('timesheet/', views.get_timesheets_view, name='get_timesheets'),
    # path('profile/', views.profile_view, name='profile'),
    path('manageproject/', views.manageproject_view, name='manageproject'),
    path('edittimesheet/',views.get_emp_summaries_view, name='get_emp_summaries'),
    path('logout/', views.logout_view, name='logout'),
]
