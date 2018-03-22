from django.urls import path
from . import views


app_name = 'supervisor'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('project/', views.project_view, name='project'),
    # path('timesheet/', views.timesheet_view, name='timesheet_view'),
    # path('profile/', views.profile_view, name='profile'),
    path('manageproject/', views.manageproject_view, name='manageproject'),
    # path('edittimesheet/',views.edit_timesheet, name='edittimesheet'),
    path('logout/', views.logout_view, name='logout'),
]
