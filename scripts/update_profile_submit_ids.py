
import os

file_path = r"c:\Users\user\Desktop\Deree\Fall Semester 2025\Capstone\ICT-4879_Capstone-Project_Orfanidis-main\ICT-4879_Capstone-Project_Orfanidis-main\accounts\templates\accounts\profile.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Form
old_form = '<form action="{% url \'submit_testimonial\' %}" method="POST">'
new_form = '<form id="submit-testimonial-form" action="{% url \'submit_testimonial\' %}" method="POST">'

if old_form in content:
    content = content.replace(old_form, new_form)
    print("Replaced Submit Form tag")
else:
    print("Submit Form tag not found")

# Replace Textarea
old_textarea = '<textarea name="message" class="form-control mb-2" rows="3" placeholder="Share your story..."></textarea>'
new_textarea = '<textarea id="submit-testimonial-msg" name="message" class="form-control mb-2" rows="3" placeholder="Share your story..."></textarea>'

if old_textarea in content:
    content = content.replace(old_textarea, new_textarea)
    print("Replaced Submit Textarea")
else:
    print("Submit Textarea not found")

# Replace Button Container
old_btn_div = '<div class="text-center mt-3"><button class="btn btn-outline-brand-orange rounded-pill px-4">Submit</button></div>'
new_btn_div = '<div id="submit-btn-container" class="text-center mt-3"><button id="submit-testimonial-btn" type="button" onclick="submitTestimonialAjax()" class="btn btn-outline-brand-orange rounded-pill px-4">Submit</button></div>'

if old_btn_div in content:
    content = content.replace(old_btn_div, new_btn_div)
    print("Replaced Submit Button Container")
else:
    print("Submit Button Container not found")
    # Debug
    # print(content[content.find("submit_testimonial"):content.find("submit_testimonial")+500])

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
