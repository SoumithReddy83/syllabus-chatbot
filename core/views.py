from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from .forms import SyllabusUploadForm
from django.contrib import messages
from .models import Syllabus
from django.db.models import Q
from .forms import AskQuestionForm
from .utils import talk_llm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ForgotUsernameForm
from django.contrib.auth.forms import PasswordResetForm





def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect after successful login
    else:
        form = UserLoginForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user

    if user.role == 'professor':
        syllabi = Syllabus.objects.filter(professor=user)
        return render(request, 'core/professor_dashboard.html', {'syllabi': syllabi})

    elif user.role == 'student':
        return render(request, 'core/student_dashboard.html')

    elif user.role == 'admin':
        return render(request, 'core/admin_dashboard.html')

    else:
        return redirect('search_syllabus')  # If some unknown role

@login_required
def upload_syllabus(request):
    if request.user.role != 'professor':
        return redirect('dashboard')  # Only professors can upload

    if request.method == 'POST':
        form = SyllabusUploadForm(request.POST, request.FILES)
        if form.is_valid():
            syllabus = form.save(commit=False)
            syllabus.professor = request.user
            syllabus.save()
            messages.success(request, 'Syllabus uploaded successfully!')
            return redirect('dashboard')
    else:
        form = SyllabusUploadForm()
    return render(request, 'core/upload.html', {'form': form})

def search_syllabus(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Syllabus.objects.filter(
            Q(department__icontains=query) |
            Q(course_number__icontains=query) |
            Q(course_name__icontains=query)
        )

    return render(request, 'core/search.html', {'results': results, 'query': query})


@login_required
def ask_question(request, syllabus_id):
    try:
        syllabus = Syllabus.objects.get(id=syllabus_id)
    except Syllabus.DoesNotExist:
        return redirect('search_syllabus')

    answer = None

    if request.method == 'POST':
        form = AskQuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question']
            context = f"Syllabus: {syllabus.course_name} ({syllabus.course_number})\nDepartment: {syllabus.department}\n\nQuestion: {question_text}"
            answer = talk_llm(context)
    else:
        form = AskQuestionForm(initial={'syllabus_id': syllabus.id})

    return render(request, 'core/ask_question.html', {'form': form, 'syllabus': syllabus, 'answer': answer})

def home(request):
    return render(request, 'core/home.html')


@login_required
def view_syllabus(request, syllabus_id):
    try:
        syllabus = Syllabus.objects.get(id=syllabus_id)
    except Syllabus.DoesNotExist:
        return redirect('search_syllabus')

    return render(request, 'core/view_syllabus.html', {'syllabus': syllabus})





def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            # In real world, send email here
            messages.success(request, 'If an account exists with that email, a password reset link has been sent.')
            return redirect('login')
    else:
        form = PasswordResetForm()
    return render(request, 'core/forgot_password.html', {'form': form})

def forgot_username(request):
    if request.method == 'POST':
        form = ForgotUsernameForm(request.POST)
        if form.is_valid():
            # In real world, lookup username by email and email it
            messages.success(request, 'If an account exists with that email, your username has been sent.')
            return redirect('login')
    else:
        form = ForgotUsernameForm()
    return render(request, 'core/forgot_username.html', {'form': form})