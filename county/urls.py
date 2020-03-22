from django.urls import path
from county import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('<int:county_id>/', views.data, name='data'),
    path('<int:county_id>/mail/', views.mail_signup, name='mail_signup'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('<int:state_id>/rankings/', views.county_rankings, name='county_rankings'),
    path('us_rankings/', views.state_rankings, name='state_rankings'),
    path('hello/', views.hello),
]
