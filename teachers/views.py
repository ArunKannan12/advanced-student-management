from django.shortcuts import render,redirect, get_object_or_404
from .forms import AssignmentForm
from django.contrib import messages
# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Teacher,Assignment,StudentAssignment,Attendance
from django.core.exceptions import ObjectDoesNotExist
from student.models import Student
from django.utils import timezone


@login_required
def teacher_dashboard(request):
    try:
        teacher = Teacher.objects.get(user=request.user)
        assignments = Assignment.objects.filter(teacher=teacher)
    except ObjectDoesNotExist:
        messages.error(request, 'No teacher profile available. Please contact support or create your profile.')
        return render(request, 'teachers/dashboard.html')

    assignment_status = []

    for assignment in assignments:
        student_assignments = assignment.studentassignment_set.all()
        total_students = student_assignments.count()
        completed_students = student_assignments.filter(is_completed=True).count()

        # Determine the status of the assignment (Completed or Pending)
        if completed_students == total_students:
            status = "Completed"
        else:
            status = "Pending"

        assignment_status.append({
            'assignment': assignment,
            'status': status,
            'completed_students': completed_students,
            'total_students': total_students
        })

    return render(request, 'teachers/dashboard.html', {
        'assignments': assignments,
        'teacher': teacher,
        'assignment_status': assignment_status
    })
@login_required
def teacher_assignments(request):
    teacher = Teacher.objects.get(user=request.user)
    assignments = Assignment.objects.filter(teacher=teacher)
    return render(request, 'teachers/assignments.html', {'assignments': assignments})

@login_required
def create_assignment(request):
    teacher = Teacher.objects.get(user=request.user)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.teacher = teacher
            assignment.save()
            form.save_m2m()
            for student in assignment.students.all():
                StudentAssignment.objects.create(student=student, assignment=assignment)
            if assignment.students.count() == 0:
                all_students = Student.objects.exclude(user__role='admin').exclude(user__role='teacher')
                assignment.students.set(all_students)
                for student in all_students:
                    StudentAssignment.objects.create(student=student, assignment=assignment)
            return redirect('teacher_assignments')
    else:
        form = AssignmentForm()
    return render(request, 'teachers/create_assignment.html', {'form': form})


@login_required
def update_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user.teacher)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('teacher_assignments')
    else:
        form = AssignmentForm(instance=assignment)
    
    return render(request, 'teachers/update_assignment.html', {'form': form, 'assignment': assignment})

@login_required
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user.teacher)
    
    assignment.delete()
    return redirect('teacher_assignments')

@login_required
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, teacher=request.user.teacher)
    return render(request, 'teachers/assignment_detail.html', {'assignment': assignment})

@login_required
def teacher_submissions(request):
    teacher = request.user.teacher  # Assuming user is linked to Teacher model
    assignments = Assignment.objects.filter(teacher=teacher)

    completed_submissions = StudentAssignment.objects.filter(
        assignment__in=assignments,
        is_completed=True
    ).select_related('student', 'assignment')

    # Find students who are assigned but haven't completed
    pending_submissions = []
    for assignment in assignments:
        assigned_students = assignment.students.all()  # many-to-many students field
        for student in assigned_students:
            if not StudentAssignment.objects.filter(student=student, assignment=assignment, is_completed=True).exists():
                pending_submissions.append({'student': student, 'assignment': assignment})

    context = {
        'completed_submissions': completed_submissions,
        'pending_submissions': pending_submissions,
    }
    return render(request, 'teachers/teacher_submissions.html', context)


# View to display today's attendance for all students
def view_today_attendance(request):
    today = timezone.now().date()
    # Get all attendance records for today
    attendance_records = Attendance.objects.filter(date=today)
    
    # You could also filter by class or other criteria if needed
    return render(request, 'teachers/view_today_attendance.html', {
        'attendance_records': attendance_records,
        'today': today
    })

# View to display attendance for a specific student
def view_student_attendance(request):
    attendance_records = Attendance.objects.all()
    
    return render(request, 'teachers/view_student_attendance.html', {
        'attendance_records': attendance_records,
        
    })
