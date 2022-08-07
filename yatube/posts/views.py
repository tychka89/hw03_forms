from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Group, User
from .forms import PostForm


number_of_elements: int = 10


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': post_list,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    username = get_object_or_404(User, username=username)
    profile_post_list = (Post.objects.filter(author=username)
                         .order_by('-pub_date'))
    paginator = Paginator(profile_post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = f'Профайл пользователя {username.get_full_name()}'
    number_of_posts = profile_post_list.count()
    is_profile = True

    context = {
        'page_obj': page_obj,
        'profile': profile_post_list,
        'username': username,
        'title': title,
        'number_of_posts': number_of_posts,
        'is_profile': is_profile
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    username = get_object_or_404(User, id=post.author_id)
    number_of_posts = Post.objects.filter(author=username).count()
    group = post.group
    title = post.text[:30]
    context = {
        'post': post,
        'username': username,
        'title': title,
        'number_of_posts': number_of_posts,
        'group': group
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', post.author.username)
    context = {
        'form': form
    }
    return render(request, 'posts/create_post.html', context)


def post_edit(request, post_id):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:post_detail', post_id)
    post = Post.objects.get(pk=post_id)
    form = PostForm(instance=post)
    is_edit = True
    context = {
        'form': form,
        'is_edit': is_edit,
        'post': post
    }
    return render(request, 'posts/create_post.html', context)

"""Уважаемый Макисм, не давайте мне, пожалуйста, очень сложных заданий(
    Мне было очень сложно сделать это, я почти впала в депрессию и так до конца и не поняла, как работает моя программа
           Ваша студентка"""
           