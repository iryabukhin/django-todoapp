from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Todo


def index(request):
    items = []
    filter = None

    # Get only the user-specific todo items.
    if request.user.is_authenticated:
        filter = request.GET.get("filter")

        items = filter_results(request.user, filter)

    return render(request, "index.html", {"items": items, "filter": filter})


def filter_results(user, filter):
    if filter == "completed":
        completed = True
    elif filter == "pending":
        completed = False
    else:
        completed = False

    return Todo.objects.filter(user=user, completed=completed)


@login_required
def create(request):
    return render(request, "form.html", {"form_type": "create"})


@login_required
def save(request):
    title = request.POST.get("title")
    description = request.POST.get("description")
    form_type = request.POST.get("form_type")
    id = request.POST.get("id")

    if title is None or title.strip() == "":
        messages.error(request, "Item not saved. Please provide the title.")
        return redirect(request.META.get("HTTP_REFERER"))

    if form_type == "create":
        todo = Todo.objects.create(title=title, description=description, created_at=timezone.now(), user=request.user)
        print("New Todo created: ", todo.__dict__)
    elif form_type == "edit" and id.isdigit():
        todo = Todo.objects.get(pk=id)
        print("Got todo item: ", todo.__dict__)

        todo.title = title
        todo.description = description

        todo.save()
        print("Todo updated: ", todo.__dict__)

    messages.info(request, "Todo  Saved.")
    return redirect("index")


@login_required
def edit(request, id):

    todo = Todo.objects.get(pk=id)

    if request.user.id != todo.user.id:
        messages.error(request, "You are not authorized to edit this todo item.")
        return redirect("index")

    return render(request, "form.html", {"form_type": "edit", "todo": todo})


@login_required
def delete(request, id):
    # Fetch todo item by id
    todo = Todo.objects.get(pk=id)
    print("Got todo item: ", todo.__dict__)

    if request.user.id == todo.user.id:
        messages.info(request, "Todo Item has been deleted.")
        todo.delete()
        return redirect("index")

    messages.error(request, "You are not authorized to delete this todo item.")
    return redirect("index")
