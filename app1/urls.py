from django.urls import path
from . import views

urlpatterns = [
    path('', views.reg_log),
    path('registration', views.registration),
    path('login', views.login),
    path('wishes', views.main),
    path('display_stats', views.display),
    path('make_a_wish', views.make_a_wish),
    path('make_a_wish_page', views.make_a_wish_page),
    path('edit_page/<int:wish_id>', views.edit_page),
    path('grant_wish/<int:wish_id>', views.grant_wish),
    path('remove_wish/<int:wish_id>', views.remove_wish),
    path('edit/<int:wish_id>', views.edit),
    path('like/<int:wish_id>', views.like),
    path('loging_out', views.loging_out),
]
