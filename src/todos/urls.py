from django.urls import path, re_path
from . import views, views_api, auth_views

urlpatterns = [
    re_path(r"^$", views.index, name="index"),

    path("todo/create/", views.TodoCreateView.as_view(), name="todo-create"),
    path("todo/<int:pk>/update", views.TodoUpdateView.as_view(), name="todo-update"),
    path("todo/<int:pk>/delete", views.TodoDeleteView.as_view(), name="todo-delete"),
    path("todo/<int:id>/complete", views.complete_task, name="todo-complete"),

    path("api/todos/<int:pk>", views_api.TodoItemView.as_view(), name="api_todo_item"),
    path("api/todos", views_api.TodoListView.as_view(), name="api_todo_list"),

    path("login", auth_views.login, name="login"),
    path("login/submit", auth_views.login_submit, name="login-submit"),
    path("signup/submit", auth_views.signup_submit, name="signup-submit"),
    path("logout", auth_views.logout, name="logout"),
]
