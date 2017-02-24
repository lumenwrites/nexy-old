from django.http import JsonResponse
from posts.models import Post

from .models import Post


def posts_stream(request):
    posts = Post.objects.all()

    stream = []
    for post in posts:
        data = {}
        data['@context'] = 'http://nexy.io/feed/posts/new'
        data['id'] = post.get_absolute_url()
        data['type'] = 'Article'
        data['name'] = post.title
        data['content'] = post.body
        data['attributedTo'] = 'http://nexy.io/@rayalez'
        # json_data = json.dumps(data)
        stream.append(data)
    
    # return HttpResponse(stream)
    return JsonResponse(stream, safe=False)


