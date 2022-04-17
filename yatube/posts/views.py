from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, Group, User, Comment, Follow
from .forms import PostForm, CommentForm


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page,
                                          'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    '''post_list = Post.objects.filter(group=group).all()'''
    post_list = Post.objects.prefetch_related('group').filter(
        group__exact=group)
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
    post_list = Post.objects.prefetch_related('author').filter(
        author__exact=profile)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'profile.html', {'page': page, 'profile': profile,
                                            'paginator': paginator})


def post_view(request, username, post_id):
    profile = get_object_or_404(User, username=username)
    post = Post.objects.get(pk=post_id)
    items = Comment.objects.filter(post_id=post_id).all()
    flag = False  # флаг формы добавления комментария
    return render(request, 'post.html', {'profile': profile, 'post': post,
                                         'items': items, 'flag': flag})


def add_comment(request, username, post_id):
    post = Post.objects.get(pk=post_id)
    items = Comment.objects.filter(post_id=post_id).all()
    flag = True  # флаг формы добавления комментария
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(f'/{username}/{post_id}/')
        return render(request, 'post.html', {'profile': post.author,
                                             'post': post, 'form': form,
                                             'flag': flag})
    form = CommentForm()
    return render(request, 'post.html', {'profile': post.author, 'post': post,
                                         'form': form, 'items': items,
                                         'flag': flag})


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


@login_required
def follow_index(request):
    authors = User.objects.get(
        pk=request.user.id).follower.all().values_list('author', flat=True)
    post_list = Post.objects.filter(author_id__in=authors).all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page,
                                           'paginator': paginator})


@login_required
def profile_follow(request, username):
    user = User.objects.get(username=username)
    if request.user != user:
        Follow.objects.create(user_id=request.user.id, author_id=user.id)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    user = User.objects.get(username=username)
    follow = Follow.objects.filter(user_id=request.user.id, author_id=user.id)
    follow.delete()
    return redirect('profile', username=username)


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    return render(request, 'misc/500.html', status=500)
