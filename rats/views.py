from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import UserForm, ProjForm, ResidencyForm, AttendanceForm
from .models import *

# Create your views here.
def toHomeURL(request):
    return redirect('home')

def home(request):
    residencies = Residency.objects.filter(user=request.user)
    attendances = Attendance.objects.filter(user=request.user)
    projects = Project.objects.filter(user=request.user)
    return render(request, 'rats/home.html',{'projects':projects, 'residencies':residencies, 'attendances':attendances})

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            return redirect('login')

    else:
        form = UserForm()
    return render(request,'registration/register.html',{'UserForm' : form})

def toLoginURL(request):
    return redirect('login')

################### RESIDENCY MANAGEMENT MODULE ###################
def residency(request):
    residencies = Residency.objects.filter(user=request.user).order_by('date')#.order_by('-due_date')
    return render(request, 'rats/residency.html', {'residencies':residencies})

def res_detail(request,pk):
    res = get_object_or_404(Residency, pk=pk)
    return render(request, 'rats/res_detail.html', {'res':res})

@login_required
def res_new(request):
    if request.method == "POST":
        form = ResidencyForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.user = request.user
            res.save()
            return redirect ('res_detail', pk=res.pk)
    else:
        form = ResidencyForm()
    return render(request, 'rats/res_edit.html', {'form': form})

@login_required
def res_edit(request, pk):
    res = get_object_or_404(Residency, pk=pk)
    if request.method == "POST":
        form = ResidencyForm(request.POST, instance=res)
        if form.is_valid():
            res = form.save(commit=False)
            res.user = request.user
            res.save()
            return redirect('res_detail', pk=res.pk)
    else:
        form = ResidencyForm(instance=res)
    return render(request, 'rats/res_edit.html', {'form': form})

@login_required
def res_remove(request, pk):
    res = get_object_or_404(Residency, pk=pk)
    res.delete()
    return redirect('residency')

################### ATTENDANCE LOGGING MODULE ###################
def attendance(request):
    attendances = Attendance.objects.filter(user=request.user).order_by('-residency__date')
    return render(request, 'rats/attendance.html', {'attendances':attendances})

def att_detail(request,pk):
    att = get_object_or_404(Attendance, pk=pk)
    return render(request, 'rats/att_detail.html', {'att': att})
    
@login_required
def att_new(request):
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            att = form.save(commit=False)
            att.user = request.user
            att.save()
            return redirect ('att_detail', pk=att.pk)
    else:
        form = AttendanceForm()
    return render(request, 'rats/att_edit.html', {'form': form})

@login_required
def att_edit(request, pk):
    att = get_object_or_404(Attendance, pk=pk)
    if request.method == "POST":
        form = AttendanceForm(request.POST, instance=att)
        if form.is_valid():
            att = form.save(commit=False)
            att.user = request.user
            att.save()
            return redirect('att_detail', pk=att.pk)
    else:
        form = AttendanceForm(instance=att)
    return render(request, 'rats/att_edit.html', {'form': form})

@login_required
def att_remove(request, pk):
    att = get_object_or_404(Attendance, pk=pk)
    att.delete()
    return redirect('attendance')


################### TEAM MANAGEMENT MODULE ###################
def teams(request):
    return render(request, 'rats/teams.html')

def team_detail(request,pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'rats/team_detail.html', {'team': team})

def team_member_detail():
    team_member = get_object_or_404(User, pk=pk)
    return render(request, 'rats/team_member_detail.html', {'team_member':team_member})

################### PROJECT MANAGEMENT MODULE ###################
def projects(request):
    projects = Project.objects.filter(user=request.user).order_by('due_date')
    return render(request, 'rats/projects.html', {'projects':projects})

def proj_detail(request,pk):
    proj = get_object_or_404(Project, pk=pk)
    return render(request, 'rats/proj_detail.html', {'proj': proj})

@login_required
def proj_new(request):
    if request.method == "POST":
        form = ProjForm(request.POST)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.user = request.user
            #due_date = form.cleaned_data['due_date']
            proj.save()
            return redirect('proj_detail', pk=proj.pk)
    else:
        form = ProjForm()
    return render(request, 'rats/proj_edit.html', {'form': form})

@login_required
def proj_edit(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjForm(request.POST, instance=proj)
        if form.is_valid():
            proj = form.save(commit=False)
            proj.user = request.user
            proj.save()
            return redirect('proj_detail', pk=proj.pk)
    else:
        form = ProjForm(instance=proj)
    return render(request, 'rats/proj_edit.html', {'form': form})

@login_required
def proj_remove(request, pk):
    proj = get_object_or_404(Project, pk=pk)
    proj.delete()
    return redirect('projects')


