from django.shortcuts import render, get_object_or_404, redirect
from .models import Program, ProgramExercise, UserProgramActivity
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def program_detail(request, program_id):
    # Get the program the user clicked
    program = get_object_or_404(Program, id=program_id)

    # Security Check: Program 1 is free, others require premium
    if program.id != 1:
        if not request.user.is_authenticated:
            # User dislikes forced login page, so we warn and redirect home
            messages.warning(request, "You have to be a Premium Member to access this program.")
            return redirect("home")
        
        # 2. Check if user has permission
        # Safely check for profile existence to avoid errors
        has_profile = hasattr(request.user, 'profile')
        is_member = request.user.profile.is_member if has_profile else False

        # Allow if member OR admin/staff
        if not is_member and not request.user.is_superuser and not request.user.is_staff:
             # Warn user about premium requirement instead of forcing upgrade page
            messages.warning(request, "You have to be a Premium Member to access this program.")
            return redirect("home")

    # --- TRACK VIEW/ENROLLMENT ---
    if request.user.is_authenticated:
        # We record this as an "enrollment" or unique view
        UserProgramActivity.objects.get_or_create(
            user=request.user,
            program=program
        )

    # Try to get the user's fitness preferences
    profile = getattr(request.user, "profile", None)

    # Exercises that belong to this program
    all_exercises = ProgramExercise.objects.filter(program=program).select_related("exercise")

    # If user has no profile, return all the available exercises
    if not profile:
        return render(request, "workouts/program_detail.html", {
            "program": program,
            "exercises": all_exercises,
        })

    # User preferences
    focus = profile.focus_body_part
    goal = profile.goal
    ex_type = profile.exercise_type

    # Strict match, meaning the exercise must match ALL preferences
    strict_matches = all_exercises.filter(
        exercise__body_part=focus,
        exercise__goal=goal,
        exercise__exercise_type=ex_type
    )

    # If strict matches exist, use them
    if strict_matches.exists():
        exercises_to_show = strict_matches

    else:
        
        # At least 2 preferences must match 
        strong_matches = []

        for pe in all_exercises:
            ex = pe.exercise
            match_count = 0

            # Count how many preferences match
            if ex.body_part == focus:
                match_count += 1
            if ex.goal == goal:
                match_count += 1
            if ex.exercise_type == ex_type:
                match_count += 1

            # Only keep exercises matching 2 or more
            if match_count >= 2:
                strong_matches.append(pe)

        # If we found strong matches then make sure that the system shows them
        if strong_matches:
            exercises_to_show = strong_matches

        else:
            # Partial match meaning that the exercise matches ANY preference
            partial_matches = all_exercises.filter(
                Q(exercise__body_part=focus) |
                Q(exercise__goal=goal) |
                Q(exercise__exercise_type=ex_type)
            )

            # If partial matches exist, use them
            if partial_matches.exists():
                exercises_to_show = partial_matches
            else:
                # If nothing matched, all the available exercises are shown
                exercises_to_show = all_exercises

    # Render to the front end
    return render(request, "workouts/program_detail.html", {
        "program": program,
        "exercises": exercises_to_show,
    })
