from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()

class Athlete(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    sport_type = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    team = models.CharField(max_length=255, blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='athlete_profiles/', blank=True, null=True)
    contact_info = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Performance(models.Model):
    athlete = models.OneToOneField(Athlete, on_delete=models.CASCADE)
    training_schedule = models.CharField(max_length=255, default="22-26 March")
    score = models.IntegerField(default=0)
    heart_rate = models.IntegerField(default=72)  # Default BPM

    def __str__(self):
        return f"{self.athlete.name} - Performance"

class Certificate(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='certificates')
    name = models.CharField(max_length=255)
    issuing_organization = models.CharField(max_length=255)
    issue_date = models.DateField()
    expiry_date = models.DateField(blank=True, null=True)
    certificate_file = models.FileField(upload_to='certificates/')
    certificate_image = models.ImageField(upload_to='certificate_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.athlete.name}"
    

class AthleteProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # Allow blank images

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.profile_picture:
            self.profile_picture = 'profile_pics/default.png'  # Ensure this file exists in MEDIA_ROOT
        super().save(*args, **kwargs)


class Event(models.Model):
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="organized_events")
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    entry_fee = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rules = models.TextField()
    participants = models.ManyToManyField(CustomUser, blank=True, related_name="joined_events")

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=255)
    sport = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    members = models.ManyToManyField(CustomUser, blank=True, related_name="teams")

    def __str__(self):
        return self.name

class TrainerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="trainer_profile")
    expertise = models.CharField(max_length=255)
    certifications = models.TextField(blank=True)
    experience = models.IntegerField(default=0)
    availability = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    posted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posted_jobs")
    location = models.CharField(max_length=255, blank=True)
    applicants = models.ManyToManyField(CustomUser, blank=True, related_name="job_applications")

class Scholarship(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField()
    organization = models.CharField(max_length=255)
    applicants = models.ManyToManyField(CustomUser, blank=True, related_name="applied_scholarships")
    