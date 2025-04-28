from django import forms
from teachers.models import StudentAssignment

class StudentAssignmentForm(forms.ModelForm):
    class Meta:
        model = StudentAssignment
        fields = ['submitted_file']  # Only the file field for submission
        submitted_file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the 'submitted_file' required only if the student hasn't submitted yet
        if not self.instance.is_completed:
            self.fields['submitted_file'].required = True
        else:
            self.fields['submitted_file'].required = False
