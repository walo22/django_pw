from django.views.generic import ListView , CreateView ,UpdateView ,DeleteView
from django.urls import reverse_lazy , reverse
from . import models
from . import forms 
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ProjectListView(LoginRequiredMixin, ListView):
   model = models.Project
   template_name = 'project/list.html' # القوالب
   paginate_by = 6
    
   def get_queryset(self):
      query_set = super().get_queryset()
      where = {}
      q = self.request.GET.get('q',None)
      if q :
         where['title_icontains'] = q 
      return query_set.filter(**where)   

#لازم له مسار 
class ProjectCreateView(LoginRequiredMixin, CreateView) : # يرث من قريت فيو
   model = models.Project
   form_class = forms.ProjectCreateForm  # الاستماره 
   template_name = 'Project/create.html'
   success_url = reverse_lazy('Project_list') # رابط الصفحه الريسيه او قائمه المشاريع



class ProjectUpdateView(LoginRequiredMixin, UpdateView) :
   model = models.Project
   form_class = forms.ProjectUpdateForm
   template_name = 'project/update.html'
   success_url = reverse_lazy('Project_list')
    

   def get_succrss_url(self):           #ايدي المشروع args  
      return reverse('Project_update' , args=[self.object.id])


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
   model = models.Project
   template_name = 'project/delete.html'
   success_url=  reverse_lazy('Project_list')


class TaskCreateView(LoginRequiredMixin, CreateView): #انشاء المهمه 
   model = models.Task
   fields =['project', 'description']  #الحقول ووصف
   http_method_names = ['post']  # 


   def get_success_url(self):
      return reverse('Project_update' , args=[self.object.project.id ])
    




class TaskUpdateView(LoginRequiredMixin, UpdateView):
   model = models.Task
   fields = ['is_completed']
   http_method_names = ['post']


   def get_success_url(self):
      return reverse('Project_update' , args=[self.object.project.id ])
    



class TaskDeleteView(LoginRequiredMixin, DeleteView):
   model = models.Task
  

   def get_success_url(self):
      return reverse('Project_update' , args=[self.object.project.id ])

