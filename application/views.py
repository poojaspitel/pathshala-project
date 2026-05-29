from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Student
from .forms import StudentForm
from datetime import datetime

def hello_world(request):
    return render(request, 'application/hello_world.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'application/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    total_students = Student.objects.count()
    recent_students = Student.objects.all()[:5]
    context = {
        'total_students': total_students,
        'recent_students': recent_students,
    }
    return render(request, 'application/dashboard.html', context)

@login_required(login_url='login')
def student_list(request):
    query = request.GET.get('search', '')
    students = Student.objects.order_by('admission_date', 'id')
    if query:
        students = students.filter(
            first_name__icontains=query
        ) | Student.objects.filter(
            last_name__icontains=query
        ) | Student.objects.filter(
            contact_no__icontains=query
        ) | Student.objects.filter(
            email__icontains=query
        )
    else:
        students = Student.objects.order_by('admission_date', 'id')
    
    context = {
        'students': students,
        'search_query': query,
    }
    return render(request, 'application/student_list.html', context)

@login_required(login_url='login')
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('student_list')
    else:
        form = StudentForm()
    
    context = {'form': form}
    return render(request, 'application/student_form.html', context)

@login_required(login_url='login')
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully!')
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    
    context = {'form': form, 'student': student, 'is_edit': True}
    return render(request, 'application/student_form.html', context)

@login_required(login_url='login')
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    if request.method == 'POST':
        name = f"{student.first_name} {student.last_name}"
        student.delete()
        messages.success(request, f'Student "{name}" deleted successfully!')
        return redirect('student_list')
    
    context = {'student': student}
    return render(request, 'application/student_confirm_delete.html', context)

@login_required(login_url='login')
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    context = {'student': student}
    return render(request, 'application/student_detail.html', context)
