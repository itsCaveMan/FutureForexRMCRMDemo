from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.dashboard),
    path('dashboard/', views.dashboard),

    path('clients/', views.Clients.as_view()),

    path('client/', views.Client.as_view()),
    path('client/<int:client_id>', views.Client.as_view()),

    path('request_document/', views.RequestDocument.as_view()),

    path('client_request/', views.ClientSubmitDocument.as_view()),
    path('client_request/<str:token_uuid>', views.ClientSubmitDocument.as_view()),

]
