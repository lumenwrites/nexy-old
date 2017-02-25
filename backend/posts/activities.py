import requests

from django.http import HttpResponse, JsonResponse

from core.models import Source
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



def posts_fetch(request):
    sources = Source.objects.all()

    posts = []
    for source in sources:
        r = requests.get(url=source.url)
        posts_list = r.json()
        for post in posts_list:
            title = post['name']
            content = post['content']
            source = post['@context']
            url = post['id']
            author = post['attributedTo']        
    
            post = Post(title=title,
                        body=content,
                        url=url)
            posts.append(post)
        
        
    return HttpResponse(posts)
