from django.contrib import admin
from django.urls import path
from . import views

# ve service
from .servicesViews.ValidateBloodRequestAPIView import ValidateBloodRequestAPIView
from .servicesViews.reply_views import ReplyCreateAPIView
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
    path('receiveAlertes/', views.AlerteReceiveListCreateAPIView.as_view() ),
    path('receiveAlertes/<uuid:id>/', views.AlerteReceiveRetrieveUpdateDestroyAPIView.as_view() ),

    path('blood_bags/', views.BloodBagListCreateAPIView.as_view(), name='bloodbag-list'),
    path('blood_bags/<uuid:id>/', views.BloodBagRetrieveUpdateDestroyAPIView.as_view(), name='bloodbag-detail'),

    path('bloodRequests/', views.BloodRequestListCreateAPIView.as_view(), name='bloodrequest-list'),
    path('bloodRequests/<uuid:id>/', views.BloodRequestRetrieveUpdateDestroyAPIView.as_view(), name='bloodrequest-detail'),
    
    path('requests/<uuid:request_id>/validate/', ValidateBloodRequestAPIView.as_view(), name='validate-blood-request'),
    path('alerts/<uuid:alert_id>/reply/', ReplyCreateAPIView.as_view(), name='reply-alert'),
]
