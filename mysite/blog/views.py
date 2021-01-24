from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect, get_object_or_404
from blog.models import Post, BlogComment
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from blog.templatetags import extras
from django.contrib.auth.models import User


# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all().order_by('-timeStamp')
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)
    # return HttpResponse("This is blog")


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    post.views = post.views + 1
    post.save()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)
    # return HttpResponse(f'This is blog:{slug}')


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentsno = request.POST.get('parentsno')
        if parentsno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentsno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")



