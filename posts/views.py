from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from django.urls import reverse_lazy

from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)

from .models import Post, Status
# Create your views here.

class PostListView(ListView):
    template_name = 'posts/list.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published_status = Status.objects.get(name="publisher")
        context["post_list"] = Post.objects.filter(
            status=published_status
        ).order_by("creat_on").reverse()
        return context

class DraftPostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        draft_status = Status.objects.get(name="draft")
        context["post_list"] = Post.objects.filter(
            status=draft_status
        ).filter(
            author=self.request.user
            ).order_by("creat_on").reverse()
        return context
    
class ArchivePostListView(LoginRequiredMixin, ListView):
    template_name = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archive_status = Status.objects.get(name="archive")
        context["post_list"] = Post.objects.filter(
            status=archive_status
        ).filter(
            author=self.request.user
            ).order_by("creat_on").reverse()
        return context



class PostDetailView(DetailView):
    template_name = 'posts/detail.html'
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'posts/new.html'
    model = Post
    fields = ['title','subtitle','body']

    def form_valid(self, form):
        form.instance.author = self.request.user
        draft_status = Status.object.get(name="draft")
        form.instance.status = draft_status
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'posts/edit.html'
    model = Post
    fields = ['title','subtitle','body', "status"]

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'posts/delete.html'
    model = Post
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user
