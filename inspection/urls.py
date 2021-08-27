from django.urls import path
from . import views

app_name = 'inspection'

urlpatterns = [
    path('dash', views.home, name='home'),
    path('', views.check, name='check'),
    path('register', views.register, name='register'),
    path('sigin', views.sigin, name='sigin'),
    path('camerap', views.camera, name='camera'),
    # path('test', views.test, name='test'),
    path('step2', views.step2, name='step2'),
    path('cong', views.cong, name='cong'),
    path('step3', views.step3, name='step3'),
    path('start_inspection', views.start_inspection, name='start_inspection'),
    path('reportlist', views.reportlist, name='reportlist'),
    path('report', views.report, name='report'),
    path('test',views.test,name="test")
]
