from django.urls import path

from .views import (
    CoachClients, NewClientsWithFormsAPI,
    AdminAndOperatorForm,
    HealsCheckAPI, AllClients, NewClientsCoach,
    VisitTable
)

urlpatterns = [
    path('clients-date/', CoachClients.as_view()),
    path('', HealsCheckAPI.as_view()),
    path('forms/', NewClientsWithFormsAPI.as_view()),
    path('client-list/', AdminAndOperatorForm.as_view()),
    path('client-all-list/', AllClients.as_view()),
    path('new-clients/', NewClientsCoach.as_view()),
    path('visit/', VisitTable.as_view()),
]
