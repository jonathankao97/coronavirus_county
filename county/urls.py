from django.urls import path
from county import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('<int:county_id>/', views.data, name='data'),
    path('<int:county_id>/mail/', views.mail_signup, name='mail_signup'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('hello/', views.hello),
]
