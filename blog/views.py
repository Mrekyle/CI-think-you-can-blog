from django.shortcuts import render
from django.views import generic
from .models import Post

# Create your views here.


class PostList(generic.ListView):
    """
    A class based view allows the individual views to inherit from each other
    allowing us to have resusable code. Unlike in function based views.
    """
    model = Post
    # Ordering the query by the date that the blog posts were created
    # status=1 allows only the 'approved' posts to be displayed to the user
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    # Saying what template to render all the blog posts onto 
    template_name = 'index.html'
    paginate_by = 6
