
from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('home', views.index, name="home"),
    path('', views.redirect_to_home, name="redirect_to_home"),
    path('qualityCheck', views.quality_check_page, name="quality_check_page"),
    path('results', views.results_page, name="results_page"),
    path('rotate_motor', views.rotate_motor, name="rotate_motor"),
    path('align_camera', views.align_camera, name="align_camera"),


    path('save_img_on_server', views.save_img_on_server, name="save_img_on_server"),
    path('get_bottle_details', views.get_bottle_details, name="get_bottle_details"),
    # path('command/populate_db/defects', views.populateDB, name="populateDB"),
    path('inspect', views.inspect, name="inspect"),
    
    path('team', views.team, name="team"),
    path('faqs', views.faqs, name="faqs"),
    path('about', views.about, name="about"),
    path('generateEtamuReportView/', views.generateEtamuReportView, name="generateEtamuReportView"), 
    path('emailEtamuReportView/', views.emailEtamuReportView, name="emailEtamuReportView"), 
    path('img_model_inspect', views.img_model_inspect, name="img_model_inspect"),
    
    
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
]