# student/views.py
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student
from teachers.models import Assignment,StudentAssignment
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .forms import StudentAssignmentForm
from datetime import date

@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
        print(student.user.email)
        # Filter assignments where the logged-in student is in the ManyToManyField
        assignments = Assignment.objects.filter(students=student)
        student_assignments = StudentAssignment.objects.filter(student=student, assignment__in=assignments)
        total_assignments = assignments.count()
        print(assignments)
       
        
    except ObjectDoesNotExist:
        # Show a message if no student object is found
        messages.error(request, 'No student profile available. Please contact support or create your profile.')
        # Render the dashboard template without the student data
        return render(request, 'students/dashboard.html')

    # Render the dashboard template with student and assignments data
    return render(request, 'students/dashboard.html', {'student': student,'assignments':assignments,'student_assignments':student_assignments,'total_assignments':total_assignments})



def student_assignments(request):
    students = Student.objects.get(user=request.user)
    assignments = Assignment.objects.filter(students=students)
    return render(request, 'students/assignments.html', {'assignments': assignments})


@login_required
def submit_assignment(request, assignment_id):
    student = Student.objects.get(user=request.user)
    assignment = Assignment.objects.get(id=assignment_id)
    student_assignment, created = StudentAssignment.objects.get_or_create(student=student, assignment=assignment)
    
    if request.method == 'POST':
        student_assignment.is_completed = True
        
        # If a file is submitted, save the file
        if 'submission_file' in request.FILES:
            student_assignment.submitted_file = request.FILES['submission_file']
            student_assignment.submitted_at = timezone.now()  # Save submission time
        
        student_assignment.save()
        return redirect('student_dashboard')

    return render(request, 'students/submit_assignment.html', {'assignment': assignment})


@login_required
def student_assignment_detail(request, assignment_id):
    try:
        # Get the assignment and the logged-in student's information
        assignment = get_object_or_404(Assignment, id=assignment_id)
        student = Student.objects.get(user=request.user)

        # Check if the student has already submitted this assignment
        student_assignment, created = StudentAssignment.objects.get_or_create(
            student=student, assignment=assignment)

        # Handle POST request for file submission
        if request.method == 'POST' and not student_assignment.is_completed:
            form = StudentAssignmentForm(request.POST, request.FILES, instance=student_assignment)
            if form.is_valid():
                student_assignment = form.save(commit=False)
                student_assignment.submitted_at = timezone.now()  # Set submission timestamp
                student_assignment.is_completed = True  # Mark as completed
                student_assignment.save()
                messages.success(request, 'Assignment submitted successfully.')
                return redirect('student_dashboard')  # Redirect back to dashboard

        else:
            form = StudentAssignmentForm(instance=student_assignment)

        # Render assignment submission form if the student hasn't submitted yet
        return render(request, 'students/assignment_detail.html', {
            'assignment': assignment,
            'student_assignment': student_assignment,
            'form': form,
            'today': date.today(),

        })

    except Assignment.DoesNotExist:
        messages.error(request, "Assignment not found.")
        return redirect('student_dashboard')
    
@login_required
def delete_submission(request, submission_id):
    # Fetch StudentAssignment instead of Assignment
    student = request.user.student  # Assuming the user is logged-in as a student
    submission = get_object_or_404(StudentAssignment, id=submission_id, student=student)

    if request.method == 'POST':
        # Delete the uploaded file
        if submission.submitted_file:
            submission.submitted_file.delete(save=False)

        # Mark as not completed
        submission.is_completed = False
        submission.submitted_file = None
        submission.submitted_at = None
        submission.save()

        messages.success(request, 'Your submission has been deleted successfully.')
        return redirect('student_dashboard')

    messages.error(request, 'Invalid request.')
    return redirect('student_dashboard')