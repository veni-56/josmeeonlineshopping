from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.auth_landing_view, name='auth_landing'),
    
    path('phone-verification/', views.phone_verification_view, name='phone_verification'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('addresses/', views.address_list_view, name='address_list'),
    path('addresses/add/', views.address_create_view, name='address_create'),
    path('addresses/<int:pk>/edit/', views.address_edit_view, name='address_edit'),
    path('addresses/<int:pk>/delete/', views.address_delete_view, name='address_delete'),
    
    path('seller/documents/upload/', views.upload_seller_documents_view, name='upload_seller_documents'),
    path('seller/documents/', views.seller_documents_view, name='seller_documents'),
]
