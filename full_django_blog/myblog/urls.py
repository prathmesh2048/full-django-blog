from django.contrib import admin
from django.urls import path, include, reverse

from .models import Post
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

from . import views
app_name = 'myblog'
urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('detail/<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('detail/<int:pk>/update', PostUpdateView.as_view(), name='update'),
    path('detail/new', PostCreateView.as_view(), name='create'),
    path('detail/<int:pk>/delete', PostDeleteView.as_view(), name='delete'),
    path('profile/', views.profile, name='profile')
]

# the template that it expects is just a form that ask are you sure to delete the post
# this template has a name 'post_confirm_delete'
