from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('submit-review/', views.submit_review, name='submit_review'),
        path('submit-enquiry/', views.submit_enquiry, name='submit_enquiry'),
]