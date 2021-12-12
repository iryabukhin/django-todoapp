from django import forms

from todos.models import Todo


class DateInput(forms.DateInput):
    input_type = "date"


class TodoCreateForm(forms.ModelForm):

    title = forms.CharField(max_length=255, required=True)
    description = forms.CharField(required=False, widget=forms.widgets.Textarea)
    due_date = forms.DateInput()
    priority = forms.IntegerField(label="Priority", max_value=100, required=False)

    class Meta:
        model = Todo
        fields = ("title", "description", "due_date", "priority")
        widgets = {
            "due_date": DateInput()
        }


class TodoUpdateForm(TodoCreateForm):

    completed = forms.CheckboxInput()

    class Meta:
        model = Todo
        fields = ("title", "description", "due_date", "priority", "completed")
        widgets = {
            "due_date": DateInput()
        }


