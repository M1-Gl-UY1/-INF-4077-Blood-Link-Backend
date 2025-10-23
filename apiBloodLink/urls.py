from django.contrib import admin
from django.urls import path
from . import views
# api doctor
urlpatterns = [
    # End point for doctor
    path('doctors/', views.DoctorListCreateAPIView.as_view() ),
    path('doctors/<uuid:id>/', views.DoctorRetrieveUpdateDestroyAPIView.as_view() ),
    
    #  End point for BloodBank
    path('bloodBanks/', views.BloodBankListCreateAPIView.as_view() ),
    path('bloodBanks/<uuid:id>/', views.BloodBankRetrieveUpdateDestroyAPIView.as_view() ),
    
    # End Point for     path('bloodTransactions/', views.BloodTransactionListCreateAPIView.as_view() ),
    path('bloodTransactions/', views.BloodTransactionListCreateAPIView.as_view() ),
    path('bloodTransactions/<uuid:id>/', views.BloodTransactionRetrieveUpdateDestroyAPIView.as_view() ),
    
    #End point for Alert
    path('alerts/', views.AlertListCreateAPIView.as_view() ),
    path('alerts/<uuid:id>/', views.AlertRetrieveUpdateDestroyAPIView.as_view() ),

        #End point for provider
    path('providers/', views.ProviderListCreateAPIView.as_view() ),
    path('providers/<uuid:id>/', views.ProviderRetrieveUpdateDestroyAPIView.as_view() ),
    
        #End point for provider
    path('receiveAlertes/', views.AlerteReceiveListAPIView.as_view() ),
    path('receiveAlertes/<uuid:id>/', views.AlerteReceiveRetrieveUpdateDestroyAPIView.as_view() ),
]