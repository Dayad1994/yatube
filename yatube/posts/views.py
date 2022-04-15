from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, Group, User
from .forms import PostForm


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page,
                                          'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group=group).order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'group.html', {'group': group, 'page': page,
                                          'paginator': paginator})


@login_required
def new_post(request):
    content = {'title_name': 'Добавить запись', 'btn_name': 'Добавить'}
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
        return render(request, 'new.html', {'form': form})
    form = PostForm()
    return render(request, 'new.html', {'form': form, 'content': content})


def profile(request, username):
    profile = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=profile).order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'page': page, 'profile': profile,
                                            'paginator': paginator})


def post_view(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = Post.objects.get(pk=post_id)
    return render(request, 'post.html', {'profile': profile, 'post': post})


@login_required
def post_edit(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = Post.objects.get(pk=post_id)
    content = {'title_name': 'Редактировать запись', 'btn_name': 'Сохранить'}
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST or None, files=request.FILES or None,
                            instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect(f'/{username}/{post_id}/')
            return render(request, 'new.html', {'form': form, 'post': post,
                                                'profile': profile})
        form = PostForm(instance=post)
    else:
        return redirect(f'/{username}/{post_id}/')
    return render(request, 'new.html', {'form': form, 'content': content,
                                        'post': post, 'profile': profile})
