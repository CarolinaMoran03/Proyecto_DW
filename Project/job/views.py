from django.forms import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from .models import Job, Mode, Skills, Company, Position, City, VisitCounter, Postulacion, Profile  # Cambié Address y Skill
from job.forms import JobForm
from django.views.decorators.csrf import csrf_exempt, csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Subquery, Case, When, Value, CharField
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import json
import time
import os




# Create your views here.

class ListJobsView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'job/listJob.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["background"] = "bg-slate-100"	
        

        counter = VisitCounter.objects.get(id=1)
        context['visit_count'] = counter.count

        return context
    
    def get_queryset(self):
        user = self.request.user
        latest_postulation = Postulacion.objects.filter(
            job=OuterRef('pk'),
            usuario=user
        ).order_by('-fecha_postulacion')
        
        return Job.objects.annotate(
            postulation_status=Case(
                When(user=user, then=Value('')),  # Si el usuario es el creador, estado vacío
                default=Subquery(latest_postulation.values('estado')[:1]),
                output_field=CharField()
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["background"] = "bg-slate-100"	
        
        counter = VisitCounter.objects.get(id=1)
        context['visit_count'] = counter.count

        return context

class CreateJobView(LoginRequiredMixin, CreateView):
    template_name = "job/formJob.html"
    model = Job
    form_class = JobForm
    
    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy('jobdescription', args=[self.object.pk])

class JobDetailView(DetailView):
    model = Job
    template_name = 'job/job_detail.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job' ] = self.get_object()
        context['user'] = self.request.user
        print(context["user"].id)
        print(context["job"].user)
        print(context['user'].is_superuser)
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch postulations for this job
        context['postulaciones'] = Postulacion.objects.filter(job=self.object, estado='pendiente')
        return context
    


class EditJobView(LoginRequiredMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'job/job_edit.html'  
    success_url = reverse_lazy('job')

class DeleteJobView(DeleteView):
    model = Job
    success_url = reverse_lazy('job')  

class JobDescriptionView(LoginRequiredMixin, TemplateView):
    template_name = 'job/jobdescription.html'

    def get_jobId(self, **kwargs):
        jobId = self.kwargs.get('pk')
        return jobId
    
    def get_Job(self):
        jobId = self.get_jobId()
        job = Job.objects.get(pk=jobId)
        return job
    
    def post(self, request, pk):
        job = self.get_Job()
        descripcion = request.POST.get("description")
        if descripcion:
            job.description = descripcion
            job.save()
            return redirect('job')
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.get_Job() 
        return context


@csrf_exempt
def increment_counter(request):
    if request.method == 'POST':
        try:
            # Obtener o crear el contador
            counter, created = VisitCounter.objects.get_or_create(id=1)
            
            # Obtener el ID del navegador del usuario 
            browser_id = request.POST.get('browser_id')
            if not browser_id:
                return JsonResponse({'error': 'Browser ID no proporcionado'}, status=400)
            
            # aqui se Obtiene la dirección IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            
            #Aqui se conprueba si el navegador ya visitó en las últimas 24 horas
            time_threshold = timezone.now() - timedelta(hours=24)
            browser_visit = BrowserVisit.objects.filter(
                browser_id=browser_id,
                ip_address=ip_address,
                last_visit__gte=time_threshold
            ).first()
            
            if not browser_visit:
                # Si no hay visita reciente, crear una nueva y incrementar el contador
                BrowserVisit.objects.create(
                    browser_id=browser_id,
                    ip_address=ip_address
                )
                counter.increment()
                
            return JsonResponse({'count': counter.count})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@require_http_methods(["GET"])
def get_counter(request):
    try:
        counter = VisitCounter.objects.get(id=1)
        return JsonResponse({'count': counter.count})
    except VisitCounter.DoesNotExist:
        return JsonResponse({'count': 0})


@csrf_exempt
def add_item(request, item_type):
    if request.method == 'POST':
        description = request.POST.get('new_item')
        
        if description:
            if item_type == 'company':
                photo = request.FILES.get('companyImage')
                new_item = Company.objects.create(description=description, photo=photo)
            elif item_type == 'address':
                new_item = City.objects.create(description=description, province=None, address="") 
            elif item_type == 'skills':
                new_item = Skills.objects.create(description=description)
            elif item_type == 'position':
                new_item = Position.objects.create(description=description)
            elif item_type == 'mode':
                new_item = Mode.objects.create(description=description)
            else:
                return JsonResponse({'success': False, 'error': 'Tipo de item no válido'}, status=400)

            return JsonResponse({
                'success': True,
                'id': new_item.id,
                'description': new_item.description
            })
        else:
            return JsonResponse({'success': False, 'error': 'Falta la descripción'}, status=400)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)


def vista_empleo(request, pk):
    job = get_object_or_404(Job, pk=pk)
    postulaciones = Postulacion.objects.filter(job=job)
    return render(request, 'vista_empleo.html', {'object': job, 'postulaciones': postulaciones})

@require_POST
def actualizar_estado_postulacion(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    nuevo_estado = request.POST.get('estado')
    if nuevo_estado in ['aprobado', 'rechazado']:
        postulacion.estado = nuevo_estado
        postulacion.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@require_POST
def crear_postulacion(request, job_id):
    print(f"Recibida solicitud de postulación para job_id: {job_id}")
    job = get_object_or_404(Job, pk=job_id)
    if Postulacion.objects.filter(usuario=request.user, job=job).exists():
        print("Usuario ya se ha postulado")
        return JsonResponse({'status': 'error', 'message': 'Ya te has postulado a este empleo'})
    
    print("Creando nueva postulación")
    Postulacion.objects.create(usuario=request.user, job=job)
    print("Postulación creada exitosamente")
    return JsonResponse({'status': 'success'})

@require_POST
def update_profile_photo(request):
    if request.FILES.get('photo'):
        try:
            profile, created = Profile.objects.get_or_create(user=request.user)
            
            # Asegúrate de que el directorio existe
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'profile_photos')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            # Actualiza la foto y guarda
            profile.photo = request.FILES['photo']
            profile.save()
            
            # Devuelve la URL de la imagen
            return JsonResponse({
                'success': True,
                'photo_url': profile.photo.url
            })
        except Exception as e:
            print(f"Error al actualizar la foto: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'No se proporcionó ninguna foto'})

@login_required
@require_POST
def delete_profile_photo(request):
    try:
        profile = request.user.profile
        if profile.photo:
            profile.photo.delete(save=False)  # Elimina el archivo físico
            profile.photo = None    # Limpia la referencia en la base de datos
            profile.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def get_counter(request):
    return JsonResponse({'count': request.user.profile.visit_count})

@login_required
@require_POST
def increment_counter(request):
    profile = request.user.profile
    profile.visit_count += 1
    profile.save()
    return JsonResponse({'count': profile.visit_count})