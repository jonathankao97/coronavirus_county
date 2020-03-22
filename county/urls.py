from django.urls import path
from county import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('search/', views.search, name='search'),
    path('<int:county_id>/', views.data, name='data'),
    path('mail/', views.mail, name='mail')
]
