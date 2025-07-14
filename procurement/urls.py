from django.urls import path
from . import views

app_name = 'procurement'

urlpatterns = [
    path('', views.tender_list_view, name='tender_list'),
    path('create/', views.tender_create_view, name='tender_create'),
    path('<uuid:tender_id>/', views.tender_detail_view, name='tender_detail'),
    path('<uuid:tender_id>/documents/upload/', views.tender_document_upload_view, name='tender_document_upload'),
] 