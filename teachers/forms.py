from django import forms
from .models import Assignment
from student.models import Student

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'students']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['students'].required = False
        # Filter the students queryset to only show relevant students
        self.fields['students'].queryset =Student.objects.exclude(user__role='admin').exclude(user__role='teacher') 
        # self.fields['students'].queryset = Student.objects.all()  # Filter if needed
        self.fields['students'].widget = forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})  # Multiple selection checkbox