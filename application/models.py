from django.db import models
from datetime import date

class Student(models.Model):
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

    SHIVA_DEEKSHA_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    # Student Details
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100, default='Indian')
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    # Parent/Guardian Details
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    contact_no = models.CharField(max_length=10)
    whatsapp_no = models.CharField(max_length=10, blank=True)
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

    # Health Information
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, blank=True)
    medical_conditions = models.TextField(blank=True)
    allergies = models.TextField(blank=True)

    # Additional Info
    shiva_deeksha = models.CharField(max_length=3, choices=SHIVA_DEEKSHA_CHOICES, default='No')
    declaration_accepted = models.BooleanField(default=False)

    # System Fields
    admission_date = models.DateField(auto_now_add=True)
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
