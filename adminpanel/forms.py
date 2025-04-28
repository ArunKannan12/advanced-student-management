from django import forms
from student.models import Student  # Import the Student model
from teachers.models import Teacher,Assignment
from authentication.models import CustomUser  # Replace 'yourapp' with the actual app where your CustomUser model is located
class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.email
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['user', 'roll_no', 'class_name', 'parent_name']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Exclude users with the 'admin' role
        self.fields['user'].queryset = CustomUser.objects.exclude(role='admin')  # Assuming you have a 'role' field for users
    # Set the queryset for the custom user model
    user = CustomModelChoiceField(
        queryset=CustomUser.objects.all(),  # Get all CustomUser objects
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

    # Optional: Customizing the labels
    user.label = 'Student User'
    roll_no.label = 'Roll Number'
    class_name.label = 'Class Name'
    parent_name.label = 'Parent Name'


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['user', 'employee_id', 'department']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
        }
        user = CustomModelChoiceField(
        queryset=CustomUser.objects.all(),  # Get all CustomUser objects
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class AssignmentForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Assignment
        fields = ['teacher', 'title', 'description', 'due_date', 'students']


class RoleUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'})
        }