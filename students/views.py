from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

# ADD STUDENT
@login_required
def add_student(request):
    form = StudentForm()
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_students')
    return render(request, 'add.html', {'form': form})

# VIEW STUDENTS
@login_required
def view_students(request):
    students = Student.objects.all()
    return render(request, 'view.html', {'students': students})

# UPDATE STUDENT
@login_required
def update_student(request, id):
    student = get_object_or_404(Student, id=id)
    form = StudentForm(instance=student)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('view_students')
    return render(request, 'update.html', {'form': form})

# DELETE STUDENT
@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('view_students')



def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('view_students')
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login')



# ✅ GET API
@csrf_exempt
def api_get_students(request):
    if request.method == "GET":
        students = list(Student.objects.all().values())
        return JsonResponse(students, safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=405)


# ✅ POST API
@csrf_exempt
def api_add_student(request):
    if request.method == "POST":
        data = json.loads(request.body)

        Student.objects.create(
            name=data['name'],
            email=data['email'],
            age=data['age'],
            course=data['course'],
            joined_date=data['joined_date']
        )

        return JsonResponse({"message": "Student added successfully"})
    return JsonResponse({"error": "Invalid request method"}, status=405)


# ✅ PUT API (FIXED)
@csrf_exempt
def api_update_student(request, id):
    if request.method == "PUT":
        data = json.loads(request.body)
        student = Student.objects.get(id=id)

        student.name = data['name']
        student.email = data['email']
        student.age = data['age']
        student.course = data['course']
        student.joined_date = data['joined_date']
        student.save()

        return JsonResponse({"message": "Student updated successfully"})
    return JsonResponse({"error": "Use PUT method"}, status=405)


# ✅ DELETE API (FIXED)
@csrf_exempt
def api_delete_student(request, id):
    if request.method == "DELETE":
        student = Student.objects.get(id=id)
        student.delete()

        return JsonResponse({"message": "Student deleted successfully"})
    return JsonResponse({"error": "Use DELETE method"}, status=405)