from django import forms
from student.models import Student
from teachers.models import Teacher, Assignment
from authentication.models import CustomUser

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.email

class StudentForm(forms.ModelForm):
    user = CustomModelChoiceField(
        queryset=CustomUser.objects.all(),  # You will fix queryset inside __init__
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    roll_no = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Roll Number'})
    )
    class_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Class Name'})
    )
    parent_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Parent Name'})
    )

    class Meta:
        model = Student
        fields = ['user', 'roll_no', 'class_name', 'parent_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show non-admin users in the dropdown
        self.fields['user'].queryset = CustomUser.objects.exclude(role='admin')
        
        # Optional: Clean Labels (this looks cleaner than setting labels outside fields)
        self.fields['user'].label = 'Student User'
        self.fields['roll_no'].label = 'Roll Number'
        self.fields['class_name'].label = 'Class Name'
        self.fields['parent_name'].label = 'Parent Name'

class TeacherForm(forms.ModelForm):
    user = CustomModelChoiceField(
        queryset=CustomUser.objects.all(),  # You will fix queryset inside __init__
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Teacher
        fields = ['user', 'employee_id', 'department']
        widgets = {
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Employee ID'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Department'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude admin users if needed (optional)
        self.fields['user'].queryset = CustomUser.objects.exclude(role='admin')
        self.fields['user'].label = 'Teacher User'
        self.fields['employee_id'].label = 'Employee ID'
        self.fields['department'].label = 'Department'

class AssignmentForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Assignment
        fields = ['teacher', 'title', 'description', 'due_date', 'students']
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Description'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class RoleUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'})
        }
