from django.shortcuts import render,redirect
from .models import Post,Comment,Tag,Reply
from .forms import CommentForm
from django.shortcuts import get_object_or_404

def post_list(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request,'blog/posts.html',context)

def post_detail(request, slug):
    post = get_object_or_404(Post,slug__iexact = slug)
    comments = Comment.objects.all()
    replies = Reply.objects.all()
    
    if request.method == "POST":
        comment=Comment.objects.create(user=request.user,post=post,body=request.POST.get('body'))
        return redirect('post',slug=post.slug)
    context = {'post':post,'comments':comments,'replies':replies}
    return render(request,'post_detail.html',context)
