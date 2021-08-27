from django.urls import path
from . import views

app_name = 'inspection'

urlpatterns = [
    path('', views.signin, name='base'),
    path('register', views.register, name='register'),
    path('signin', views.signin, name='signin'),
    path('dashboard', views.home, name='home'),
    path('configuration', views.configuration, name='cong'),
    path('start_inspection', views.start_inspection, name='start_inspection'),
    path('reportlist', views.reportlist, name='reportlist'),
    path('report', views.report, name='report'),
    path('test',views.test,name="test"),
    path("logout", views.logout, name="logout")
]
