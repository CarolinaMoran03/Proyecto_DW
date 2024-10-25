from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('job/', ListJobsView.as_view(), name="job"),
    path('create/job/', CreateJobView.as_view(), name="createjob"),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('job/<int:pk>/edit/', EditJobView.as_view(), name='edit_job'),
    path('job/<int:pk>/delete/', DeleteJobView.as_view(), name='delete_job'),
    path('jobdescription/<int:pk>/', JobDescriptionView.as_view(), name='jobdescription'),
    # path('add-new-item/', add_new_item, name='add_new_item'),
    path('add_<str:item_type>/', views.add_item, name='add_item'),
    path('increment-counter/', increment_counter, name='increment_counter'),
    path('get-counter/', get_counter, name='get_counter'),
    path('empleo/<int:pk>/', views.vista_empleo, name='vista_empleo'),
    path('actualizar-postulacion/<int:postulacion_id>/', views.actualizar_estado_postulacion, name='actualizar_postulacion'),
    path('crear-postulacion/<int:job_id>/', views.crear_postulacion, name='crear_postulacion'),
    path('update-profile-photo/', views.update_profile_photo, name='update_profile_photo'),
    path('delete-profile-photo/', views.delete_profile_photo, name='delete_profile_photo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)