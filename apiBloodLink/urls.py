from django.contrib import admin
from django.urls import path
from . import views

# Services
from .servicesViews.ValidateBloodRequestAPIView import ValidateBloodRequestAPIView
from .servicesViews.reply_views import ReplyCreateAPIView
from .servicesViews.initBloodTransactionViews import ValidateinitBloodTransactionViewsView

urlpatterns = [
    # ================================
    # DOCTOR
    # ================================
    path('doctors/', views.DoctorListCreateAPIView.as_view()),
    path('doctors/<uuid:id>/', views.DoctorRetrieveUpdateDestroyAPIView.as_view()),

    # ================================
    # BLOOD BANK
    # ================================
    path('bloodBanks/', views.BloodBankListCreateAPIView.as_view()),
    path('bloodBanks/<uuid:id>/', views.BloodBankRetrieveUpdateDestroyAPIView.as_view()),

    # ================================
    # BLOOD TRANSACTIONS
    # ================================
    path('getbloodTransactions/', views.BloodTransactionListCreateAPIView.as_view()),
    path('postbloodTransactions/', ValidateinitBloodTransactionViewsView.as_view()),
    path('bloodTransactions/<uuid:id>/', views.BloodTransactionRetrieveUpdateDestroyAPIView.as_view()),

    # ================================
    # BLOOD BAG
    # ================================
    path('blood_bags/', views.BloodBagListCreateAPIView.as_view(), name='bloodbag-list'),
    path('blood_bags/<uuid:id>/', views.BloodBagRetrieveUpdateDestroyAPIView.as_view(), name='bloodbag-detail'),

    # ================================
    # ALERTS
    # ================================
    path('alerts/', views.AlertListCreateAPIView.as_view()),
    path('alerts/<uuid:id>/', views.AlertRetrieveUpdateDestroyAPIView.as_view()),

    # ================================
    # PROVIDER
    # ================================
    path('providers/', views.ProviderListCreateAPIView.as_view()),
    path('providers/<uuid:id>/', views.ProviderRetrieveUpdateDestroyAPIView.as_view()),

    # ================================
    # ALERT RECEIVE
    # ================================
    path('receiveAlertes/', views.AlerteReceiveListCreateAPIView.as_view()),
    path('receiveAlertes/<uuid:id>/', views.AlerteReceiveRetrieveUpdateDestroyAPIView.as_view()),

    # ================================
    # BLOOD REQUEST
    # ================================
    path('bloodRequests/', views.BloodRequestListCreateAPIView.as_view(), name='bloodrequest-list'),
    path('bloodRequests/<uuid:id>/', views.BloodRequestRetrieveUpdateDestroyAPIView.as_view(), name='bloodrequest-detail'),
    path('requests/<uuid:request_id>/validate/', ValidateBloodRequestAPIView.as_view(), name='validate-blood-request'),
    path('alerts/<uuid:alert_id>/reply/', ReplyCreateAPIView.as_view(), name='reply-alert'),

    # ================================
    # AUTHENTIFICATION BLOODBANK
    # ================================
    path('registerBloodBank/', views.RegisterBloodBankAPIView.as_view(), name='register-bloodbank'),
    path('loginBloodBank/', views.LoginBloodBankAPIView.as_view(), name='login-bloodbank'),

    # ================================
    # AUTHENTIFICATION USER (si besoin)
    # ================================
    path('register/', views.RegisterUserAPIView.as_view(), name='register'),
    path('login/', views.LoginUserAPIView.as_view(), name='login'),
]
