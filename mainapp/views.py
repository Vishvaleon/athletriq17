from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Athlete, Certificate, Performance,AthleteProfile,Event,TrainerProfile,Team,Job,Scholarship

def splash_screen(request):
    return render(request, 'splash.html')

def onboarding(request):
    return render(request, "onboarding.html") 

@login_required
def home(request):
    return render(request, 'home.html') 


def auth_page(request):
    return render(request, 'auth.html') 

def role_selection_view(request):
    if request.method == "POST":
        selected_role = request.POST.get("role")  # Get the selected role
        if selected_role:
            request.session["user_role"] = selected_role  # Store role in session
            return redirect("athlete_dashboard")  

    return render(request, "role_selection.html")  # Re-render form if not POST

#def main_page_view(request):
   # return render(request, "main_page.html")

@csrf_exempt  # ❗ Remove this in production
def dashboard(request):
    if request.method == "POST":
        try:
            if request.content_type == "application/json":
                data = json.loads(request.body)
                role = data.get("role", "None")
            else:
                role = request.POST.get("role", "None")

            return JsonResponse({"message": f"Role {role} selected!"})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def sportsperson_dashboard(request):
    return render(request, "sportsperson.html")

@login_required
def organizer_dashboard(request):
    return render(request, "organizer.html")

@login_required
def trainer_dashboard(request):
    return render(request, "trainer.html")


def is_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(is_admin)
def edit_athlete(request, id):
    athlete = get_object_or_404(Athlete, id=id)

    if request.method == "POST":
        athlete.name = request.POST["name"]
        athlete.age = request.POST["age"]
        athlete.sport_type = request.POST["sport_type"]
        athlete.country = request.POST["country"]
        athlete.save()
        return redirect("admin_dashboard")

    return render(request, "edit_athlete.html", {"athlete": athlete})

@login_required
@user_passes_test(is_admin)
def delete_athlete(request, id):
    athlete = get_object_or_404(Athlete, id=id)
    athlete.delete()
    return redirect("admin_dashboard")

@login_required
@user_passes_test(is_admin)
def edit_certificate(request, id):
    certificate = get_object_or_404(Certificate, id=id)

    if request.method == "POST":
        certificate.name = request.POST["name"]
        certificate.issuing_organization = request.POST["issuing_organization"]
        certificate.issue_date = request.POST["issue_date"]
        certificate.save()
        return redirect("admin_dashboard")

    return render(request, "edit_certificate.html", {"certificate": certificate})

@login_required
@user_passes_test(is_admin)
def delete_certificate(request, id):
    certificate = get_object_or_404(Certificate, id=id)
    certificate.delete()
    return redirect("admin_dashboard")

@login_required
def athlete_dashboard(request):
    """Ensure the athlete profile exists before rendering the dashboard."""
    athlete_profile, created = AthleteProfile.objects.get_or_create(user=request.user)

    events = Event.objects.all()
    teams = Team.objects.all()
    trainers = TrainerProfile.objects.all()
    jobs = Job.objects.all()
    scholarships = Scholarship.objects.all()

    context = {
        "athlete_profile": athlete_profile,
        "events": events,
        "teams": teams,
        "trainers": trainers,
        "jobs": jobs,
        "scholarships": scholarships
    }
    return render(request, "athlete_dashboard.html", context)



def get_athlete_data(request):
    athlete = Athlete.objects.first()  # ✅ Get first athlete (modify as needed)
    certificates = Certificate.objects.filter(athlete=athlete).values("name", "issuing_organization", "issue_date")

    data = {
        "name": athlete.name,
        "training": "22-26 March Training",
        "performance": "Score: 229",
        "heart_rate": 72,
        "certificates": list(certificates),
    }
    return JsonResponse(data)

def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    # Add logic to register the user for the event
    return redirect('dashboard')

def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    # Add application logic here
    return redirect('dashboard')

def apply_scholarship(request, scholarship_id):
    scholarship = get_object_or_404(Scholarship, id=scholarship_id)
    # Application logic here (e.g., saving application to database)
    return redirect('dashboard') 
