from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.dashboard, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('clients/', views.clients, name='clients'),

    path('client/', views.Client.as_view(), name='crud_client'),
    path('client/<int:client_id>', views.Client.as_view(), name='view_client'),

    path('request_document/', views.RequestDocument.as_view(), name='request_document'),

    path('client_request/', views.ClientSubmitDocument.as_view(), name='submit_document'),
    path('client_request/<str:token_uuid>', views.ClientSubmitDocument.as_view(), name='view_document_request'),

    path('thank_you/', views.thank_you, name='thank_you'),

]
