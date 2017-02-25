from django.conf.urls import url

from .views import BrowseView, TagView
from .views import PostDetailView, post_create, post_edit, post_delete
from .views import upvote, unupvote
from .activities import posts_stream, posts_fetch

urlpatterns = [
    url(r'^$', BrowseView.as_view()),
    url(r'^tag/(?P<slug>[^\.]+)/$', TagView.as_view()),
    url(r'^(?P<slug>[^\.]+)-tutorials/$', TagView.as_view()),    

    # url(r'^post/(?P<slug>[^\.]+)/edit$', PostUpdateView.as_view()),
    url(r'^post/(?P<slug>[^\.]+)/edit$', post_edit),    
    url(r'^post/(?P<slug>[^\.]+)/delete$', post_delete),
    url(r'^post/(?P<slug>[^\.]+)/$', PostDetailView.as_view(), name='post-detail'),

    url(r'^submit$', post_create),

    url(r'^upvote/$', upvote),
    url(r'^unupvote/$', unupvote),

    # Activities
    url(r'^stream/posts/$', posts_stream),
    url(r'^fetch/posts/$', posts_fetch),            
]
