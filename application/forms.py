from datetime import date

from django import forms
from .models import Student

INDIAN_STATES = [
    ('', '— Select State —'),
    ('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh', 'Arunachal Pradesh'),
    ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chhattisgarh', 'Chhattisgarh'),
    ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'),
    ('Himachal Pradesh', 'Himachal Pradesh'), ('Jharkhand', 'Jharkhand'),
    ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'),
    ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'),
    ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'),
    ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'),
    ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'),
    ('West Bengal', 'West Bengal'), ('Delhi', 'Delhi'), ('Jammu and Kashmir', 'Jammu and Kashmir'),
    ('Ladakh', 'Ladakh'), ('Puducherry', 'Puducherry'), ('Chandigarh', 'Chandigarh'),
    ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('Lakshadweep', 'Lakshadweep'), ('Other', 'Other'),
]


class StudentForm(forms.ModelForm):
    application_date = forms.DateField(
        required=True,
        initial=date.today,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'ageInput',
            'placeholder': 'Auto calculated',
            'readonly': 'readonly',
            'style': 'background:#F5EDD8;color:#8B5A1A;cursor:not-allowed;'
        })
    )
    state = forms.ChoiceField(
        choices=INDIAN_STATES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    last_class = forms.ChoiceField(
        choices=[('', '— Select —'), ('5th Standard', '5th Standard'), ('6th Standard', '6th Standard'), ('7th Standard', '7th Standard'), ('8th Standard', '8th Standard')],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'nationality', 'photo',
            'father_name', 'mother_name', 'occupation', 'contact_no', 'whatsapp_no', 'email',
            'address_line1', 'address_line2', 'city', 'state', 'pin_code',
            'last_school', 'last_class', 'year_passing', 'shiva_deeksha',
            'blood_group', 'medical_conditions', 'allergies',
            'declaration_accepted',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_tongue': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'programme': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.Select(attrs={'class': 'form-control'}),
            'mode': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'prior_knowledge': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's Name"}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Mother's Name"}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXX XXXXX'}),
            'whatsapp_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXX XXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address_line1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'House No., Street / Village'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Locality / Area'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City / Town'}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'PIN Code'}),
            'last_school': forms.TextInput(attrs={'class': 'form-control'}),
            'last_class': forms.TextInput(attrs={'class': 'form-control'}),
            'year_passing': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2025'}),
            'shiva_deeksha': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'medical_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'allergies': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'doc_birth_certificate': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'doc_marksheet': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'doc_photo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'doc_address_proof': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'doc_medical': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'doc_vedic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'doc_income': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reference_source': forms.Select(attrs={'class': 'form-control'}),
            'reference_person': forms.TextInput(attrs={'class': 'form-control'}),
            'signature': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type full name as signature'}),
            'declaration_accepted': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'first_name': 'First Name *',
            'last_name': 'Last Name *',
            'date_of_birth': 'Date of Birth *',
            'gender': 'Gender',
            'nationality': 'Nationality',
            'mother_tongue': 'Mother Tongue',
            'photo': 'Student Photograph',
            'programme': 'Programme Applying For *',
            'duration': 'Duration',
            'mode': 'Mode of Study',
            'start_date': 'Preferred Start Date',
            'prior_knowledge': 'Prior Knowledge / Experience',
            'father_name': "Father's Name *",
            'mother_name': "Mother's Name",
            'occupation': 'Occupation',
            'contact_no': 'Primary Contact Number *',
            'whatsapp_no': 'WhatsApp Number',
            'email': 'Email Address',
            'address_line1': 'Address Line 1 *',
            'address_line2': 'Address Line 2',
            'city': 'City / Town *',
            'state': 'State *',
            'pin_code': 'PIN Code',
            'last_school': 'Last School / Institution',
            'last_class': 'Highest Standard / Class Passed',
            'year_passing': 'Year of Passing',
            'shiva_deeksha': 'Shiva Deeksha (Ayyachara)',
            'blood_group': 'Blood Group',
            'medical_conditions': 'Known Medical Conditions',
            'allergies': 'Allergies / Special Requirements',
            'doc_birth_certificate': 'Birth Certificate / Proof of Age',
            'doc_marksheet': 'Last School Marksheet / Transfer Certificate',
            'doc_photo': '4 Passport-Size Photographs',
            'doc_address_proof': 'Address Proof (Aadhaar / Voter ID / Ration Card)',
            'doc_medical': 'Medical Fitness Certificate',
            'doc_vedic': 'Vedic Study Certificate (if any)',
            'doc_income': 'Income Certificate (for scholarship applicants)',
            'reference_source': 'How Did You Know About Us?',
            'application_date': 'Date of Application',
            'reference_person': 'Reference Person Name',
            'signature': 'Applicant / Parent Signature',
            'declaration_accepted': 'I / We accept the declaration and the Gurukul\'s terms and conditions.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['state'].choices = INDIAN_STATES
        self.fields['application_date'].initial = getattr(self.instance, 'admission_date', date.today()) or date.today()
        if self.instance and self.instance.pk:
            self.fields['age'].initial = self.instance.get_age()
        else:
            self.fields['age'].initial = ''
        if self.instance and self.instance.state:
            self.fields['state'].initial = self.instance.state

    def save(self, commit=True):
        student = super().save(commit=False)
        application_date = self.cleaned_data.get('application_date')
        if application_date:
            student.admission_date = application_date
        if commit:
            student.save()
        return student

