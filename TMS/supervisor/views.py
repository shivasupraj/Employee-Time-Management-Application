from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Supervisor
from accounts.models import Profile, Project, TimeSheet
from django.contrib.auth.models import User
from datetime import datetime, date
# Create your views here.

# This login_view gets the request and checks if the requested method is an get or postself.
# If the method is get return the login pageself.
# Else if post then check the credentials, if error then return to login page with message
#                                          else send the view page.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # Retrieve the profile object by using user and
        # use the profile object returned to check if the profile objects
        # is in the supervisor object. If the user is not None and returned
        # user_supervisor query set length is 1 then we login the user
        profile = Profile.objects.filter(user=user)
        if len(profile) == 0: return render(request, 'supervisor/login.html', {'error': 'Username or Password is incorrect'})
        profile = profile[0]
        user_supervisor = Supervisor.objects.filter(user=profile)
        if user is not None and (len(user_supervisor) == 1):
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return render(request, 'supervisor/view.html')
        else:
            return render(request, 'supervisor/login.html', {'error': 'Username or Password is incorrect'})
    else:
        return render(request, 'supervisor/login.html')

def logout_view(request):
    logout(request)
    return render(request, 'supervisor/login.html', {'error':'logged out succesfully'})

def project_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pass
        else:
            user = User.objects.get(username=request.user.username)
            profile = Profile.objects.filter(user=user)
            supervisor = Supervisor.objects.filter(user=profile[0])[0]
            projects = supervisor.projects.all()
            return render(request, 'supervisor/project.html', {'projects':projects})
    else:
        return render(request, 'supervisor/login.html', {'error': 'Login to access the page'})

# check if the user is logged in else return him login page
# else return the all the timesheets the user requested for a project
def get_timesheets_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
             pass
        else:
            project_id = request.GET['project_id']
            project = Project.objects.filter(id=project_id)[0]
            timesheets = TimeSheet.objects.filter(project=project)
            return render(request, 'supervisor/timesheet.html', {'timesheets':timesheets})
    else:
        return render(request, 'supervisor/login.html', {'error': 'Login to access the page'})


def get_emp_summaries_view(request):
    if request.method == 'POST':
        pass
    else:
        project_id = request.GET['project_id']
        project = Project.objects.filter(id=project_id)[0]
        timesheets = TimeSheet.objects.filter(project=project)
        emp_summaries = {}
        for timesheet in timesheets:
            if timesheet.emp_name in emp_summaries:
                emp_summaries[timesheet.emp_name] += datetime.combine(date.today(),timesheet.end_time) - datetime.combine(date.today(),timesheet.start_time)
                print(timesheet.emp_name,emp_summaries[timesheet.emp_name])
            else:
                emp_summaries[timesheet.emp_name] = datetime.combine(date.today(),timesheet.end_time) - datetime.combine(date.today(),timesheet.start_time)
                print(timesheet.emp_name,emp_summaries[timesheet.emp_name])
        return render(request, 'supervisor/Summaries.html',{'emp_summaries':emp_summaries,'project_name':project.project_name})

#check the user is logged in else return him to login page
# check if the request is POST else return the project requested
# if POST then remove/add the Selected employees from project
def manageproject_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # if the button clicked is delete_emp then delete the employees from
            # project else if add_emp then add employees to project
            if 'delete_emp' in request.POST:
                employee_ids = request.POST.getlist('employees')
                project_id = request.POST['project_id']
                project = Project.objects.filter(id=project_id)[0]
                for e_id in employee_ids:
                    project.employees.remove(e_id)
                employees = Profile.objects.all()
                employees_inproject =  project.employees.all()
                employees_could_add =  employees.difference(employees_inproject)
                return render(request, 'supervisor/manageproject.html',{'project':project, 'employees_could_add':employees_could_add,'error':'Selected users are removed'})
            elif 'add_emp' in request.POST:
                employee_ids = request.POST.getlist('employees')
                project_id = request.POST['project_id']
                project = Project.objects.filter(id=project_id)[0]
                for e_id in employee_ids:
                    project.employees.add(e_id)
                employees = Profile.objects.all()
                employees_inproject =  project.employees.all()
                employees_could_add =  employees.difference(employees_inproject)
                return render(request, 'supervisor/manageproject.html',{'project':project,'employees_could_add':employees_could_add, 'error':'Selected users are removed'})
        else:
            if 'manage_project' in request.GET:
                employees = Profile.objects.all()
                project_id = request.GET.get('project_id')
                project = Project.objects.filter(id=project_id)[0]
                employees_inproject =  project.employees.all()
                employees_could_add =  employees.difference(employees_inproject)
                return render(request, 'supervisor/manageproject.html', {'project':project, 'employees_could_add':employees_could_add})

    else:
        return render(request, 'supervisor/login.html', {'error': 'Login to access the page'})
