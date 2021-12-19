from django.urls import path, re_path
from . import views, views_api, auth_views

urlpatterns = [
    re_path(r"^$", views.TodoListView.as_view(), name="index"),

    path("todo/create/", views.TodoCreateView.as_view(), name="todo-create"),
    path("todo/<int:pk>/update", views.TodoUpdateView.as_view(), name="todo-update"),
    path("todo/<int:pk>/delete", views.TodoDeleteView.as_view(), name="todo-delete"),
    path("todo/<int:id>/complete", views.complete_task, name="todo-complete"),

    path("api/todos/<int:pk>", views_api.TodoItemView.as_view(), name="api_todo_item"),
    path("api/todos", views_api.TodoListView.as_view(), name="api_todo_list"),

    path("auth/login", auth_views.LoginView.as_view(), name="login"),
    path("auth/signup", auth_views.signup_submit, name="signup"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
]
