from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Student
from .forms import StudentForm
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
from reportlab.lib import colors
from io import BytesIO
import os

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

@login_required(login_url='login')
def student_export_pdf(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    # Create PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#8B4513'),
        spaceAfter=12,
        alignment=1
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#D4612A'),
        spaceAfter=8,
        spaceBefore=6
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#3E2723'),
    )
    
    # Title
    elements.append(Paragraph("Shree Guru Kumareshwar - Student Details", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Student Photo (if exists)
    if student.photo:
        try:
            photo_path = student.photo.path
            if os.path.exists(photo_path):
                img = RLImage(photo_path, width=1.5*inch, height=2*inch)
                photo_table = Table([[img]], colWidths=[1.5*inch])
                photo_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BORDER', (0, 0), (-1, -1), 1, colors.HexColor('#D4612A')),
                    ('PADDING', (0, 0), (-1, -1), 5),
                ]))
                elements.append(photo_table)
                elements.append(Spacer(1, 0.15*inch))
        except:
            pass
    
    # Personal Information
    elements.append(Paragraph("Personal Information", heading_style))
    personal_data = [
        ['Field', 'Details'],
        ['Name', f"{student.first_name} {student.last_name}"],
        ['Date of Birth', student.date_of_birth.strftime("%d %B %Y") if student.date_of_birth else 'N/A'],
        ['Age', f"{student.get_age()} years"],
        ['Nationality', student.nationality],
        ['Gender', student.gender],
    ]
    personal_table = Table(personal_data, colWidths=[2*inch, 4*inch])
    personal_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D4612A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5D4B6')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFFAF3')]),
    ]))
    elements.append(personal_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # Parent/Guardian Information
    elements.append(Paragraph("Parent / Guardian Details", heading_style))
    parent_data = [
        ['Field', 'Details'],
        ['Father Name', student.father_name],
        ['Mother Name', student.mother_name or 'N/A'],
        ['Occupation', student.occupation or 'N/A'],
        ['Contact Number', student.contact_no],
        ['WhatsApp Number', student.whatsapp_no or 'N/A'],
        ['Email', student.email or 'N/A'],
    ]
    parent_table = Table(parent_data, colWidths=[2*inch, 4*inch])
    parent_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D4612A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5D4B6')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFFAF3')]),
    ]))
    elements.append(parent_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # Address Information
    elements.append(Paragraph("Residential Address", heading_style))
    address_text = student.get_full_address()
    elements.append(Paragraph(address_text, normal_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Health Information
    elements.append(Paragraph("Health Information", heading_style))
    health_data = [
        ['Field', 'Details'],
        ['Blood Group', student.blood_group or 'N/A'],
        ['Medical Conditions', student.medical_conditions or 'None'],
        ['Allergies', student.allergies or 'None'],
    ]
    health_table = Table(health_data, colWidths=[2*inch, 4*inch])
    health_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#D4612A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5D4B6')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFFAF3')]),
    ]))
    elements.append(health_table)
    elements.append(Spacer(1, 0.15*inch))
    
    # Additional Information
    elements.append(Paragraph("Additional Information", heading_style))
    admission_date = student.admission_date.strftime("%d %B %Y") if student.admission_date else 'N/A'
    additional_text = f"<b>Admission Date:</b> {admission_date}<br/><b>Shiva Deeksha:</b> {student.shiva_deeksha}<br/><b>Declaration Accepted:</b> {'Yes' if student.declaration_accepted else 'No'}"
    elements.append(Paragraph(additional_text, normal_style))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    
    # Create response
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Student_{student.first_name}_{student.last_name}.pdf"'
    return response
