from django.views.generic import ListView , CreateView ,UpdateView ,DeleteView
from django.urls import reverse_lazy , reverse
from . import models
from . import forms 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

class ProjectListView(LoginRequiredMixin, ListView):
   model = models.Project
   template_name = 'project/list.html' # القوالب
   paginate_by = 6
    
   def get_queryset(self):
      query_set = super().get_queryset()
      where = {'user_id': self.request.user}
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

   def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)


class ProjectUpdateView(LoginRequiredMixin,UserPassesTestMixin ,UpdateView) :
   model = models.Project
   form_class = forms.ProjectUpdateForm
   template_name = 'project/update.html'
   #success_url = reverse_lazy('Project_list')

   def test_func(self):
      return self.get_object().user_id == self.request.user.id

   def get_succrss_url(self):           #ايدي المشروع args  
      return reverse('Project_update' , args=[self.object.id])


class ProjectDeleteView(LoginRequiredMixin,UserPassesTestMixin ,DeleteView):
   model = models.Project
   template_name = 'project/delete.html'
   success_url=  reverse_lazy('Project_list')

   def test_func(self):
      return self.get_object().user_id == self.request.user.id


class TaskCreateView(LoginRequiredMixin,UserPassesTestMixin, CreateView): #انشاء المهمه 
   model = models.Task
   fields =['project', 'description']  #الحقول ووصف
   http_method_names = ['post']  # 

   def test_func(self):
      project_id = self.request.POST.get('project', '')
      return models.Project.objects.get(pk=project_id).user_id == self.request.user.id 


   def get_success_url(self):
      return reverse('Project_update' , args=[self.object.project.id ])
    


class TaskUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
   model = models.Task
   fields = ['is_completed']
   http_method_names = ['post']


   def test_func(self):
      return self.get_object().project.user_id == self.request.user.id


   def get_success_url(self):
      return reverse('Project_update' , args=[self.object.project.id ])
    



class TaskDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
   model = models.Task
  

   def test_func(self):
      return self.get_object().project.user_id == self.request.user.id


   def get_success_url(self):
      return reverse('Project_update' , args=[self.object.project.id ])

