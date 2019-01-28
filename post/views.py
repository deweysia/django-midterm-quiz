from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from .models import Post, Comment
from .forms import CommentForm

# Create your views here.

def index(request):
	now = datetime.datetime.now()
	html = "<html><body>It is now %s.</body></html>" % now
	return HttpResponse(html)


class PostListView(ListView):
    model = Post
    template_name = "post/index.html"
    context_object_name = 'posts'
    ordering = ['-date_updated']


class PostDetailView(DetailView):
    model = Post
    template_name = "post/post.html"
    context_object_name = 'post'


class PostCreateView(CreateView):
	model = Post
	template_name = "post/create_post.html"
	fields = ['title', 'content']

class PostUpdateView(UpdateView):
	model = Post
	template_name = "post/update_post.html"
	fields = ['title', 'content']

class CommentCreateView(CreateView):
    model = Comment
    template_name = "post/create_comment.html"

    fields = ['content']

    def form_valid(self, form):
    	form.instance.post = self.request.post
    	return super().form_valid(form)



def comment(request, post_id):
	post = Post.objects.get(id=post_id)
	context = {}

	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.post = post
			new_comment.save()
			return redirect('post-detail', post_id)
		else:
			context['form'] = form
			return render(request, 'post/create_comment.html', context)
	else:
		form = CommentForm()
		context['form'] = form
		return render(request, 'post/create_comment.html', context)