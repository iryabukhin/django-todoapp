from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework.reverse import reverse_lazy
from jsonview.decorators import json_view
from todos.forms import TodoCreateForm, TodoUpdateForm
from todos.models import Todo
import json


class TodoCreateView(CreateView, SuccessMessageMixin, LoginRequiredMixin):
    model = Todo
    form_class = TodoCreateForm
    template_name = "todo_create.html"
    success_message = "Created entry successfully"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TodoUpdateView(UpdateView, SuccessMessageMixin, LoginRequiredMixin):
    model = Todo
    form_class = TodoUpdateForm
    template_name = "todo_update.html"
    success_url = reverse_lazy("index")
    success_message = "Task updated"


class TodoDeleteView(DeleteView, LoginRequiredMixin):
    model = Todo

    success_url = reverse_lazy("index")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponse(json.dumps({"success": True}), status=200, content_type="application/json")


class TodoListView(ListView, LoginRequiredMixin):
    model = Todo
    template_name = "index.html"
    context_object_name = "todos"
    login_url = "/login"
    redirect_field_name = "redirect_to"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by("-priority")


@login_required
@json_view
def complete_task(request, id):
    task = Todo.objects.get(pk=id)
    if not task:
        raise Http404("Task with id {} does not exist".format(str(id)))

    task.completed = True
    task.save()

    return {'success': True}
