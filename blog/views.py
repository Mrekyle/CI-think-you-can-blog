from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Post
from .forms import CommentForm

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


class PostDetail(View):
    """
    A manual class views method. Unlike a function based model
    we have to create everything manually by defining cariables of the methods
    we expect to use
    """

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': False,
                'liked': liked,
                'comment_form': CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "comment_form": comment_form,
                "liked": liked
            },
        )
