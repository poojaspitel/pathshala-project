#!/usr/bin/env python
# Script to update student form template with photo requirements

# Read template
with open('application/templates/application/student_form.html', 'r') as f:
    content = f.read()

# Find the photo field and add help text
old_section = '{{ form.photo }} \n                        {{ form.photo.errors }}\n                    </div>'
new_section = '''{{ form.photo }} 
                        {{ form.photo.errors }}
                        <div style="margin-top: 10px; padding: 12px; background: #FFF3E0; border: 1px solid #FFB74D; border-radius: 6px; font-size: 0.85rem; color: #E65100;">
                            <strong style="color: #FF6F00;">📷 Photo Requirements:</strong><br/>
                            • <strong>Format:</strong> JPEG, PNG, or WebP image files<br/>
                            • <strong>File Size:</strong> Maximum 2MB<br/>
                            • <strong>Dimensions:</strong> Minimum 100×100px, Maximum 2000×2000px<br/>
                            • <strong>Aspect Ratio:</strong> ID-size photos (roughly square, e.g., 2×2", 3×4")<br/>
                            • <strong>Quality:</strong> Clear, passport-style identification photo
                        </div>
                    </div>'''

if old_section in content:
    content = content.replace(old_section, new_section)
    with open('application/templates/application/student_form.html', 'w') as f:
        f.write(content)
    print('✓ Photo field help text updated successfully')
else:
    print('✗ Could not find photo section to update')
