from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    # slug:slug means that it will take the string of the
    # post name and number to form the url for the path address
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail')
]
