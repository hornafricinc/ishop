from django.urls import path

from shopowner import views
app_name='shopowner'

urlpatterns=[
    path('',views.Home.as_view(),name='index'),
    path('cus_signup/',views.createCustomerAccount,name='signup'),
    path('lipanampesaonline/', views.lipanaMpesaOnline, name='lipa'),
    path('confirmation/', views.mpesaConfirmation, name='confirmation'),
]