
import os

file_path = r"c:\Users\user\Desktop\Deree\Fall Semester 2025\Capstone\ICT-4879_Capstone-Project_Orfanidis-main\ICT-4879_Capstone-Project_Orfanidis-main\accounts\templates\accounts\profile.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Form
old_form = '<form action="{% url \'edit_testimonial\' %}" method="POST">'
new_form = '<form id="testimonial-form" action="{% url \'edit_testimonial\' %}" method="POST">'

if old_form in content:
    content = content.replace(old_form, new_form)
    print("Replaced Form tag")
else:
    print("Form tag not found")

# Replace Textarea
old_textarea = '<textarea name="message" class="form-control mb-2" rows="3">{{ testimonial.message }}</textarea>'
new_textarea = '<textarea id="testimonial-msg" name="message" class="form-control mb-2" rows="3">{{ testimonial.message }}</textarea>'

if old_textarea in content:
    content = content.replace(old_textarea, new_textarea)
    print("Replaced Textarea")
else:
    print("Textarea not found")

# Replace Button
# We need to be careful. The button line has classes.
old_btn_start = '<button class="btn btn-outline-brand-orange rounded-pill px-4 mx-2">Update</button>'
new_btn_start = '<button id="update-testimonial-btn" type="button" onclick="updateTestimonialAjax()" class="btn btn-outline-brand-orange rounded-pill px-4 mx-2">Update</button>'

if old_btn_start in content:
    content = content.replace(old_btn_start, new_btn_start)
    print("Replaced Button")
else:
    print("Button not found. Trying loose match.")
    # Maybe spaces are different?
    # Let's try regex or just manual check?
    pass

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
