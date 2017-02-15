

from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect

from .models import Post
from .forms import PostForm
from tags.models import Tag


class FilterMixin(object):
    paginate_by = 15
    def get_queryset(self):
        qs = super(FilterMixin, self).get_queryset()

        # Filter by category
        # try:
        #     selectedhubs = self.request.GET['hubs'].split(",")
        # except:
        #     selectedhubs = []

        # Filter by posttype
        posttype = self.request.GET.get('posttype')
        if posttype:
            qs = qs.filter(post_type=posttype)   
        level = self.request.GET.get('level')
        if level:
            qs = qs.filter(post_level=level)   
        price = self.request.GET.get('price')
        if price:
            qs = qs.filter(post_price=price)   

        # Filter by query
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(Q(title__icontains=query) |
                           Q(body__icontains=query) |
                           Q(author__username__icontains=query))                    




        # Sort
        # (Turns queryset into the list, can't just .filter() later
        # sorting = self.request.GET.get('sorting')
        # if sorting == 'top':
        #     qs = qs.order_by('-score')
        # elif sorting == 'new':
        #     qs = qs.order_by('-pub_date')
        # else:
        #     qs = rank_hot(qs)

        return qs

    def get_context_data(self, **kwargs):
        context = super(FilterMixin, self).get_context_data(**kwargs)
        urlstring = ""
        # Sorting
        # if self.request.GET.get('sorting'):
        #     sorting = self.request.GET.get('sorting')
        # else:
        #     sorting = "hot"
        # context['sorting'] = sorting


        # All Tags
        tags = Tag.objects.all()
        tags = Tag.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')   
        context['tags'] = tags

        # Solo Tag
        context['tag'] = self.request.GET.get('tag')


        # Query
        query = self.request.GET.get('query')
        if query:
            context['query'] = query
            urlstring += "&query=" + query            

        context['urlstring'] = urlstring

        context['submitform'] = PostForm()
        
        return context
    


class BrowseView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"



class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'    
    template_name = "posts/post-detail.html"



    



class TagView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def get_queryset(self):
        qs = super(TagView, self).get_queryset()

        # Filter by tag
        tag = Tag.objects.get(slug=self.kwargs['tag'])

        # qs = [p for p in qs if (tag in p.tags.all())]

        posts = []
        for post in qs:
            for h in post.tags.all():
                if h.slug==tag.slug:
                    posts.append(post)
        qs = posts

        return qs
        
    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        tag = Tag.objects.get(slug=self.kwargs['tagslug'])
        context['tagtitle'] = tag.title
        context['tag'] = tag
        return context    
    


# Voting
def upvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.score += 1
    post.save()
    post.author.karma += 1
    post.author.save()
    user = request.user
    user.upvoted.add(post)
    user.save()

    # Notification
    notification = Notification(from_user=request.user,
                                to_user=post.author,
                                post=post,
                                notification_type="upvote")
    notification.save()
    post.author.new_notifications = True
    post.author.save()
    return HttpResponse()

def unupvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.score -= 1
    post.save()
    post.author.karma -= 1
    post.author.save()
    user = request.user
    user.upvoted.remove(post)
    user.save()
    return HttpResponse()

    



def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.score += 1 # self upvote
            post.save()

            # request.user.upvoted.add(post)

            # Add hubs
            # post.hubs.add(*form.cleaned_data['hubs'])
            # hubs = post.hubs.all()
            
            return HttpResponseRedirect('/post/'+post.slug)
        else:
            errors = str(form.errors)
            return HttpResponseRedirect('/?error='+errors)        

    else:
        # for errors
        return render(request, 'posts/create.html', {
            'submitform':form,
        })
