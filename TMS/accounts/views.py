from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Profile, Project, TimeSheet
from django.contrib.auth.models import User
import datetime
# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return render(request, 'accounts/view.html')
        else:
            return render(request, 'accounts/login.html', {'error': 'Username or Password is incorrect'})
    else:
        return render(request, 'accounts/login.html')

def project_view(request):
    if request.user.is_authenticated:
        username = User.objects.get(username=request.user.username)
        id = request.user.id
        projects = Project.objects.filter(employees__id=id)
        return render(request, 'accounts/project.html', {'projects':projects})
    else:
        return render(request, 'accounts/login.html', {'error': 'Login to access the page'})

def timesheet_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        timesheets = TimeSheet.objects.filter(user=username)
        print(timesheets)
        return render(request, 'accounts/timesheet.html', {'timesheets':timesheets})
    else:
        return render(request, 'accounts/login.html', {'error': 'Login to access the page'})

def add_timesheet(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            timesheet = TimeSheet()
            timesheet.user = request.user.username
            timesheet.date = request.POST['date']
            timesheet.start_time = request.POST['from']
            timesheet.end_time = request.POST['to']
            timesheet.project = request.POST.get('project_name')
            timesheet.save()
            projects = Project.objects.filter(employees__id=request.user.id)
            return render(request, 'accounts/project.html', {'projects':projects})
        else:
            project_name = request.GET.get('project_name')
            return render(request, 'accounts/add_timesheet.html', {'project_name':project_name})
    else:
        return render(request, 'accounts/login.html', {'error': 'Login to access the page'})

def edit_timesheet(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            timesheet_id = request.POST.get('timesheet_id')
            timesheet = TimeSheet.objects.filter(id=timesheet_id)[0]
            timesheet.user = request.user.username
            timesheet.date = request.POST['date']
            timesheet.start_time = request.POST['from']
            timesheet.end_time = request.POST['to']
            timesheet.project = request.POST.get('project_name')
            timesheet.save()
            username = request.user.username
            timesheets = TimeSheet.objects.filter(user=username)
            return render(request, 'accounts/timesheet.html', {'timesheets':timesheets})
        else:
            timesheet_id = request.GET.get('timesheet_id')
            timesheet = TimeSheet.objects.filter(id=timesheet_id)[0]
            grace_days = datetime.datetime.now().date()-timesheet.date
            # if the requested timesheet's date to be edited is more than 13 days or 2 weeks
            # then return the timesheets apge to user saying that, he canot edit that timesheet.
            if grace_days.days > 13:
                timesheets = TimeSheet.objects.filter(user=request.user.username)
                return render(request, 'accounts/timesheet.html', {'error':'You can\'t edit your two weeks past timesheet', 'timesheets':timesheets})
            return render(request, 'accounts/edittimesheet.html', {'timesheet':timesheet})
    else:
        return render(request, 'accounts/login.html', {'error': 'Login to access the page'})

def profile_view(request):
    if request.user.is_authenticated:
        username = User.objects.get(username=request.user.username)
        profile = Profile.objects.filter(user=username)
        return render(request, 'accounts/profile.html', {'profile':profile[0]})
    else:
        return render(request, 'accounts/login.html', {'error': 'Login to access the page'})



def logout_view(request):
    logout(request)
    return render(request, 'accounts/login.html', {'error':'logged out succesfully'})
