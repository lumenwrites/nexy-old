from django.http import HttpResponse
from actstream import action
from posts.models import Post

from .models import Post


def posts_stream(request):
    posts = Post.objects.all()

    action.send(request.user, verb='reached level 10')
    stream = ""
    for post in posts:
        activity = post.title + " " + post.url
        stream += activity
    
    return HttpResponse(stream)

