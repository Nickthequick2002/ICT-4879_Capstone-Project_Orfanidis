
import os

file_path = r"c:\Users\user\Desktop\Deree\Fall Semester 2025\Capstone\ICT-4879_Capstone-Project_Orfanidis-main\ICT-4879_Capstone-Project_Orfanidis-main\accounts\templates\accounts\profile.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Target the button
old_button = '<button class="btn btn-sm btn-warning rounded-pill">Submit</button>'
new_button = '<div class="text-center mt-3"><button class="btn btn-outline-brand-orange rounded-pill px-4">Submit</button></div>'

if old_button in content:
    content = content.replace(old_button, new_button)
    print("Replaced Submit Button")
else:
    print("Submit Button not found")
    # Debug info
    # print(content[content.find("submit_testimonial"):content.find("submit_testimonial")+300])

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
