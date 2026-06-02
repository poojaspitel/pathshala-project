#!/usr/bin/env python
"""Fix student form template to add photo requirements."""

import re

# Read the template file
with open('application/templates/application/student_form.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the photo field section
old_pattern = r'(\{\{ form\.photo \}\}\s*\{\{ form\.photo\.errors \}\})'
replacement = r'''{{ form.photo }} 
                        {{ form.photo.errors }}
                        <div style="margin-top: 10px; padding: 12px; background: #FFF3E0; border: 1px solid #FFB74D; border-radius: 6px; font-size: 0.85rem; color: #E65100;">
                            <strong style="color: #FF6F00;">📷 Photo Requirements:</strong><br/>
                            • <strong>Format:</strong> JPEG, PNG, or WebP image files<br/>
                            • <strong>File Size:</strong> Maximum 2MB<br/>
                            • <strong>Dimensions:</strong> Minimum 100×100px, Maximum 2000×2000px<br/>
                            • <strong>Aspect Ratio:</strong> ID-size photos (roughly square, e.g., 2×2", 3×4")<br/>
                            • <strong>Quality:</strong> Clear, passport-style identification photo
                        </div>'''

if re.search(old_pattern, content):
    new_content = re.sub(old_pattern, replacement, content)
    with open('application/templates/application/student_form.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('✓ Photo requirements added to template')
else:
    print('Pattern not found, trying alternate approach...')
    # Try direct string replacement
    search_str = '{{ form.photo }} \n                        {{ form.photo.errors }}\n                    </div>'
    replace_str = '''{{ form.photo }} 
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
    
    if search_str in content:
        new_content = content.replace(search_str, replace_str)
        with open('application/templates/application/student_form.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print('✓ Photo requirements added to template (alternate method)')
    else:
        print('✗ Could not find photo field to update')
