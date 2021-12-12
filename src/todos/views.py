from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from rest_framework.reverse import reverse_lazy
from jsonview.decorators import json_view
from todos.forms import TodoCreateForm, TodoUpdateForm
from todos.models import Todo


class TodoCreateView(CreateView, SuccessMessageMixin, LoginRequiredMixin):
    model = Todo
    form_class = TodoCreateForm
    # http_method_names = ['POST']
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


class TodoDeleteView(DeleteView, SuccessMessageMixin, LoginRequiredMixin):
    model = Todo
    success_url = reverse_lazy("index")

    success_message = "Successfully deleted entry"


@login_required(login_url="/login")
def index(request):
    items = Todo.objects.filter(user=request.user)
    return render(request, "index.html", {"items": items})


@login_required
# @require_http_methods(["PUT"])
@json_view
def complete_task(request, id):
    task = Todo.objects.get(pk=id)
    if not task:
        raise Http404("Task with id {} does not exist".format(str(id)))

    task.completed = True
    task.save()

    return {'success': True}
