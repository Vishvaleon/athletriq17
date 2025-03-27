from django.urls import path
from .views import splash_screen, onboarding, auth_page, home,role_selection_view,edit_athlete,delete_athlete,delete_certificate,edit_certificate,athlete_dashboard,sportsperson_dashboard,organizer_dashboard,trainer_dashboard,register_event,apply_job,apply_scholarship

urlpatterns = [
    path('', splash_screen, name='splash'),
    path('onboarding/', onboarding, name='onboarding'),
    path('auth/', auth_page, name='auth_page'),
    path('home/', home, name='home'),
    path("role-selection/", role_selection_view, name="role_selection"),
    path("dashboard/", athlete_dashboard, name="athlete_dashboard"),
    path("sportsperson/", sportsperson_dashboard, name="sportsperson_dashboard"),
    path("organizer/", organizer_dashboard, name="organizer_dashboard"),
    path("trainer/", trainer_dashboard, name="trainer_dashboard"),
    #path("main/", main_page_view, name="main_page"),
    path("edit-athlete/<int:id>/", edit_athlete, name="edit_athlete"),
    path("delete-athlete/<int:id>/", delete_athlete, name="delete_athlete"),
    path("edit-certificate/<int:id>/", edit_certificate, name="edit_certificate"),
    path("delete-certificate/<int:id>/", delete_certificate, name="delete_certificate"),
    path('register-event/<int:event_id>/', register_event, name='register_event'),
    path('apply-job/<int:job_id>/', apply_job, name='apply_job'),
    path('apply-scholarship/<int:scholarship_id>/', apply_scholarship, name='apply_scholarship'),
]

