from django.shortcuts import render, get_object_or_404, redirect
from student.models import Student
from authentication.models import CustomUser
from .forms import StudentForm,TeacherForm,AssignmentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from teachers.models import Teacher,Assignment
from adminpanel.forms import RoleUpdateForm
from django.db.models import Q


def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def update_user_role(request, user_id):
    query = request.GET.get('q')
    if query:
        users = CustomUser.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        users = CustomUser.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(CustomUser, id=user_id)
        form = RoleUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('update_user_role',user_id=user_id)
    else:
        form = RoleUpdateForm()
    
    return render(request, 'adminpanel/update_user_role.html', {'form': form, 'users': users, 'query': query})



# Helper function to check if user is admin



@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    
    return render(request, 'adminpanel/dashboard.html')



@login_required
@user_passes_test(is_admin)
def student_list(request):
    students = Student.objects.select_related('user').all()
    return render(request, 'adminpanel/student_list.html', {'students': students})


@login_required
@user_passes_test(is_admin)
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'adminpanel/student_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def student_update(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'adminpanel/student_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def student_delete(request,  student_id):
    student = get_object_or_404(Student, pk=student_id)
    if request.method == 'GET':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')



@login_required
@user_passes_test(is_admin)
def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    
    # Render the student details page with the student's information
    return render(request, 'adminpanel/student_detail.html', {'student': student})



@login_required
@user_passes_test(is_admin)
def teacher_list(request):
    teachers = Teacher.objects.all()  # Get all teachers from the database
    return render(request, 'adminpanel/teacher_list.html', {'teachers': teachers})


@login_required
@user_passes_test(is_admin)
def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)  # Get a specific teacher by ID
    return render(request, 'adminpanel/teacher_detail.html', {'teacher': teacher})



@login_required
@user_passes_test(is_admin)
def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new teacher to the database
            return redirect('teacher_list')  # Redirect to teacher list
    else:
        form = TeacherForm()
    return render(request, 'adminpanel/teacher_form.html', {'form': form})



  # Assuming you have a TeacherForm
@login_required
@user_passes_test(is_admin)
def teacher_update(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)  # Get teacher by ID
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)  # Fill form with existing data
        if form.is_valid():
            form.save()  # Save the updated teacher data
            return redirect('teacher_detail', teacher_id=teacher.id)
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'adminpanel/teacher_form.html', {'form': form})



@login_required
@user_passes_test(is_admin)
def teacher_delete(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    teacher.delete()  # Delete the teacher record
    return redirect('teacher_list')  # Redirect to teacher list



@login_required
@user_passes_test(is_admin)
def assignment_list(request):
    assignments = Assignment.objects.all()  # Get all assignments from the database
    return render(request, 'adminpanel/assignment_list.html', {'assignments': assignments})


@login_required
@user_passes_test(is_admin)
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    return render(request, 'adminpanel/assignment_detail.html', {'assignment': assignment})


@login_required
@user_passes_test(is_admin)
def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new assignment
            return redirect('assignment_list')  # Redirect to the assignment list page
    else:
        form = AssignmentForm()
    return render(request, 'adminpanel/assignment_form.html', {'form': form})



@login_required
@user_passes_test(is_admin)
def assignment_update(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()  # Save the updated assignment
            return redirect('assignment_detail', assignment_id=assignment.id)
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'adminpanel/assignment_form.html', {'form': form})



@login_required
@user_passes_test(is_admin)
def assignment_delete(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    assignment.delete()  # Delete the assignment record
    return redirect('assignment_list')  # Redirect to assignment list