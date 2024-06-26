from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='main'),
    path('register-light/', views.diagnostics, name='diagnostic'),
    path('symptoms/', views.symptoms, name='symptoms'),
    path('cancer/', views.cancer, name='cancer'),
    path('pneumonia/', views.pneumonia, name='pneumonia'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)