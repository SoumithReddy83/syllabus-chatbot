from django.urls import path
from .views import login_view, logout_view, dashboard
from .views import upload_syllabus
from .views import search_syllabus
from .views import ask_question
from .views import home
from .views import view_syllabus
from .views import forgot_password, forgot_username


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('upload/', upload_syllabus, name='upload_syllabus'),
    path('search/', search_syllabus, name='search_syllabus'),
    path('ask/<int:syllabus_id>/', ask_question, name='ask_question'),
    path('', home, name='home'),
    path('view/<int:syllabus_id>/', view_syllabus, name='view_syllabus'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('forgot-username/', forgot_username, name='forgot_username'),
]
