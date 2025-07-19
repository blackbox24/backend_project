from django.shortcuts import render,  get_object_or_404,  redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,  logout,  authenticate

from .models import Blog
from .forms import BlogForm
# Create your views here.
REDIRECT_URL = "pages:admin"

def home_page(request):
    blogs = Blog.objects.all()
    template_name = "blog/index.html"
    return render(request, template_name, {"blogs":blogs})

def article_page(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    template_name = "blog/detail_blog.html"
    return render(request, template_name, {"blog":blog})

@login_required(login_url="/account/login")
def dashboard(request):
    blogs = Blog.objects.all()
    template_name = "blog/dashboard.html"
    return render(request, template_name, {"blogs":blogs})

@login_required()
def add_blog_page(request):
    if request.method == "POST":
        form = BlogForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(REDIRECT_URL)
    else:
        form = BlogForm()
    template_name = "blog/create_blog.html"
    return render(request, template_name, {"form":form})

@login_required()
def edit_blog_page(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    if request.method == "POST":
        form = BlogForm(data=request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect(REDIRECT_URL)
    else:
        form = BlogForm(instance=blog)
    template_name = "blog/edit_blog.html"
    return render(request, template_name, {"form":form})

@login_required()
def delete_blog_page(request, pk):
    blog = get_object_or_404(Blog, id=pk)
    blog.delete()
    return redirect(REDIRECT_URL)