
import os

file_path = r"c:\Users\user\Desktop\Deree\Fall Semester 2025\Capstone\ICT-4879_Capstone-Project_Orfanidis-main\ICT-4879_Capstone-Project_Orfanidis-main\accounts\templates\accounts\profile.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Target Container and Delete Button
# Previous: <div class="text-center mt-3"> ... buttons ... </div>
# But I already updated the Update button in Step 998/1004.
# The content block looks like:
# <div class="text-center mt-3">
#    <button id="update-testimonial-btn" ...>Update</button>
#    <button formaction="{% url 'delete_testimonial' %}" ...>Delete</button>
# </div>

# I'll replace the whole div block to match easier (using regex or loose logic).
# Construct "old" block roughly
old_sub = '<button formaction="{% url \'delete_testimonial\' %}" class="btn btn-outline-danger rounded-pill px-4 mx-2">Delete</button>'
new_sub = '<button id="delete-testimonial-btn" type="button" onclick="deleteTestimonialAjax()" class="btn btn-outline-danger rounded-pill px-4 mx-2">Delete</button>'

# Replace the button
if old_sub in content:
    content = content.replace(old_sub, new_sub)
    print("Replaced Delete Button")
else:
    print("Delete Button not found")
    # Debug
    # print(content[content.find("delete_testimonial")-50:content.find("delete_testimonial")+100])

# Add ID to container
# Find the container surrounding the buttons.
# Since I updated "update-testimonial-btn", I can find it and look backwards for <div ...>
# <div class="text-center mt-3">
old_div = '<div class="text-center mt-3">'
new_div = '<div id="update-btn-container" class="text-center mt-3">'

# There are TWO <div class="text-center mt-3"> !?
# One for Update form, one for Submit form?
# Submit form logic (Step 1092): replaced with <div id="submit-btn-container" ...>
# So the ONLY remaining `class="text-center mt-3"` without ID should be the Update Form container.
# BUT I must be careful.
# Does `old_div` trigger on "submit-btn-container"? No, that has ID.
# So replacing `old_div` with `new_div` SHOULD work if strict string match.

if old_div in content:
    # Check if we are inside the Update form block (near edit_testimonial)
    # I'll try to just split content or use count.
    count = content.count(old_div)
    print(f"Found {count} occurrences of div")
    content = content.replace(old_div, new_div)
    print("Replaced Div Container")
else:
    print("Div Container not found")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
