from django.urls import path
from . import views

urlpatterns = [
    path(
        'register/', views.RegisterView.as_view(), name='register'
    ),
    path(
        'login/', views.LoginView.as_view(), name='login'
    ),
    path(
        'users/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'
    ),
    path(
        'users/<int:pk>/',
          views.UserViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
            }), name='user-detail'
        ),
    path(
        'users/profile/', views.UserViewSet.as_view({'get': 'profile'}), name='user-profile'
    ),
    path(
        'users/update_profile/', views.UserViewSet.as_view({'put': 'update_profile'}),
         name='user-update-profile'
    ),
    path('users/doctors/', views.UserViewSet.as_view({'get': 'doctors'}), name='user-doctors'),
    path('users/patients/', views.UserViewSet.as_view({'get': 'patients'}), name='user-patients'),
    path(
        'patients/', views.PatientViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='patient-list'
    ),
    path(
        'patients/<int:pk>/', 
        views.PatientViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
        }),
        name='patient-detail'
    ),
    path(
        'doctors/', views.DoctorViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='doctor-list'
    ),
    path(
        'doctors/<int:pk>/', 
        views.DoctorViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
        }), name='doctor-detail'
    ),
    path(
        'doctors/<int:pk>/availability/', views.DoctorViewSet.as_view({'get': 'availability'}), 
        name='doctor-availability'
    ),
    path(
        'lab-technicians/', views.LabTechnicianViewSet.as_view({'get': 'list', 'post': 'create'}), 
        name='labtechnician-list'
    ),
    path('lab-technicians/<int:pk>/', 
    views.LabTechnicianViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
        }), name='labtechnician-detail'
    ),
    path(
        'receptionists/', views.ReceptionistViewSet.as_view({'get': 'list', 'post': 'create'}), 
        name='receptionist-list'
    ),
    path(
        'receptionists/<int:pk>/', 
        views.ReceptionistViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'
        }), name='receptionist-detail'
    ),
]