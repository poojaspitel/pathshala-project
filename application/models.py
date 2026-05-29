from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Student(models.Model):  
    MODE_CHOICES = [
        ('Residential', 'Residential (Gurukul)'),
        ('Day Scholar', 'Day Scholar'),
        ('Online', 'Online'),
    ]
    
    PROGRAMME_CHOICES = [
        ('Veda (Vedic Studies)', 'Veda (Vedic Studies)'),
        ('Vedic Chanting', 'Vedic Chanting (Kramapatha / Ghanapatha)'),
        ('Sanskrit Language', 'Sanskrit Language & Grammar (Ashtadhyayi)'),
        ('Jyotisha', 'Jyotisha (Vedic Astrology)'),
        ('Ayurveda', 'Ayurveda Foundation'),
        ('Yoga', 'Yoga & Meditation'),
        ('Vedic Mathematics', 'Vedic Mathematics'),
        ('Purohit Training', 'Purohit Training (Ritual Procedures)'),
        ('General Studies', 'General Vedic Studies'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A−'),
        ('B+', 'B+'),
        ('B-', 'B−'),
        ('O+', 'O+'),
        ('O-', 'O−'),
        ('AB+', 'AB+'),
        ('AB-', 'AB−'),
    ]
    
    REFERENCE_SOURCE_CHOICES = [
        ('Word of Mouth', 'Word of Mouth / Family'),
        ('Alumni', 'Former Student / Alumni'),
        ('Temple', 'Temple / Ashram'),
        ('Social Media', 'Social Media'),
        ('Website', 'Website'),
        ('Newspaper', 'Newspaper / Magazine'),
        ('Other', 'Other'),
    ]
    
    DURATION_CHOICES = [
        ('1 Year', '1 Year'),
        ('2 Years', '2 Years'),
        ('3 Years', '3 Years'),
        ('Short Course', 'Short Course (3–6 months)'),
    ]
    
    # Student Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    gender = models.CharField(max_length=100, default='Male')
    nationality = models.CharField(max_length=100, default='Indian')
    mother_tongue = models.CharField(max_length=100, default='Kannada')
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)
    
    # Course Details
    programme = models.CharField(max_length=100, choices=PROGRAMME_CHOICES)
    duration = models.CharField(max_length=50, choices=DURATION_CHOICES, default='1 Year')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='Residential')
    start_date = models.DateField(null=True, blank=True)
    prior_knowledge = models.TextField(blank=True)
    
    # Parent/Guardian Details
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    contact_no = models.CharField(max_length=15)
    whatsapp_no = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    
    # Address
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10, blank=True)
    
    # Previous Education
    last_school = models.CharField(max_length=255, blank=True)
    last_class = models.CharField(max_length=50, blank=True)
    year_passing = models.CharField(max_length=4, blank=True)
    percentage = models.CharField(max_length=10, blank=True)
    
    # Health Information
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, blank=True)
    medical_conditions = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    
    # Documents
    doc_birth_certificate = models.BooleanField(default=False)
    doc_marksheet = models.BooleanField(default=False)
    doc_photo = models.BooleanField(default=False)
    doc_address_proof = models.BooleanField(default=False)
    doc_medical = models.BooleanField(default=False)
    doc_vedic = models.BooleanField(default=False)
    doc_income = models.BooleanField(default=False)
    
    # Additional Info
    reference_source = models.CharField(max_length=100, choices=REFERENCE_SOURCE_CHOICES, blank=True)
    reference_person = models.CharField(max_length=100, blank=True)
    signature = models.CharField(max_length=255, blank=True)
    declaration_accepted = models.BooleanField(default=False)
    
    # System Fields
    admission_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    
    class Meta:
        ordering = ['-admission_date']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_age(self):
        today = date.today()
        age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age
    
    def get_full_address(self):
        return f"{self.address_line1}, {self.address_line2}, {self.city}, {self.state} - {self.pin_code}"
