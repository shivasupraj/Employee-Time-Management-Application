from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Supervisor
from accounts.models import Profile, Project
from django.contrib.auth.models import User
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
        user_supervisor = Supervisor.objects.filter(user=profile[0])
        if user is not None and len(user_supervisor) == 1:
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
    if request.method == 'POST':
        pass
    else:
        user = User.objects.get(username=request.user.username)
        profile = Profile.objects.filter(user=user)
        supervisor = Supervisor.objects.filter(user=profile[0])[0]
        projects = supervisor.projects.all()
        return render(request, 'supervisor/project.html', {'projects':projects})

def manageproject_view(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            employee_ids = request.POST.getlist('employees')
            project_id = request.POST['project_id']
            project = Project.objects.filter(id=project_id)[0]
            for e_id in employee_ids:
                e = project.employees.filter(id=e_id)[0]
                e.delete()
            return render(request, 'supervisor/manageproject.html',{'project':project, 'error':'Selected users are removed'})
        else:
            project_id = request.GET.get('project_id')
            project = Project.objects.filter(id=project_id)[0]
            print(project.employees.all())
            return render(request, 'supervisor/manageproject.html',{'project':project})
    else:
        return render(request, 'supervisor/login.html', {'error': 'Login to access the page'})
