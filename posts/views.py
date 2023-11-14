from django.shortcuts import render, redirect
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    posts = Post.objects.all().order_by('-id')

    context = {
        'posts' : posts,
    }

    return render(request, 'index.html', context)

def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            post.user = request.user
            post.save()
            return redirect('posts:index')
    else:
        form = PostForm()

    context = {
        'form' : form,
    }

    return render(request, 'form.html', context)

def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('posts:index')


@login_required
def likes(request, id):
    user = request.user
    post = Post.objects.get(id=id)

    # 이미 좋아요를 누른 경우
    # if post in user.like_posts.all():
    # 아래 위 코드는 아래와 같은 이유로 같은 코드다.
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    # 아래 위는 user 정보와 post정보를 동시에 저장한다는 점에서 같은 코드다.(양방향성)
    # user.like_posts.add(post)

    return redirect('posts:index')

from django.http import JsonResponse
def likes_async(request, id):
    user = request.user
    post = Post.objects.get(id=id)

    if user in post.like_users.all():
        post.like_users.remove(user)
        status = False
    else:
        post.like_users.add(user)
        status = True

    context = {
        'status' : status,
        'count' : len(post.like_users.all()),
    }

    return JsonResponse(context)


@login_required
def comment_create(request, post_id):
    form = CommentForm(request.POST)
    # article= Article.objects.get(id=id)

    if form.is_valid():
        comment = form.save(commit=False)
 
        comment.user_id = request.user.id
        comment.post_id = post_id
        comment.save()

        return redirect('posts:detail', id=post_id)

def detail(request, id):
    post = Post.objects.get(id=id)
    form = CommentForm

    context = {
        'post': post,
        'form': form,
    }
    return render(request, 'detail.html', context)

@login_required
def comment_delete(request, post_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    
    if request.user == comment.user:
        comment.delete()
    
    return redirect('posts:detail', id=post_id)

