from django.urls import path
from county import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('<int:county_id>/', views.data, name='data'),
    path('subscribe/', views.subscribe, name='signup'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('hello/', views.hello),
]
