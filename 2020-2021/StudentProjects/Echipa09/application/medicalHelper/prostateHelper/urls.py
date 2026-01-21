from django.urls import path

from . import views

app_name = 'prostateHelper'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:image_id>/analysed_image/', views.analysed_image, name='analysed_image')
]