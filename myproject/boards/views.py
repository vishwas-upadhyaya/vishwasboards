from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Board, Topic, Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from .forms import NewTopicForm,PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.utils import timezone
from django.views.generic import UpdateView,ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import math

class BoardListView(ListView):
    model=Board
    context_object_name = 'boards'
    template_name = 'home.html'

def board_topics(request,pk):
    board=get_object_or_404(Board,pk=pk)
    queryset=board.topics.order_by('-last_updated').annotate(replies=Count('posts')-1)
    page=request.GET.get('page',1)
    paginator=Paginator(queryset,7)
    try:
        topics=paginator.page(page)
    except PageNotAnInteger:
        topics=paginator.page(1)
    except EmptyPage:
        topics=paginator.page(paginator.num_pages)

    return render(request,'topics.html',{'board':board,'topics':topics})








@login_required()
def new_topic(request,pk):
    board=get_object_or_404(Board,pk=pk)

    if request.method == 'POST':
        form=NewTopicForm(request.POST)
        if form.is_valid():
            topic=form.save(commit=False)
            topic.board=board
            topic.starter=request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user

            )
            return redirect('topic_posts',pk=pk,topic_pk=topic.pk)
    else:
        form=NewTopicForm()
    return render(request, 'new_topic.html', {'board': board,'form':form})

def topic_posts(request,pk,topic_pk):
   topic=get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
   session_key = 'viewed_topic_{}'.format(topic.pk)
   if not request.session.get(session_key, False):
       topic.views += 1
       topic.save()
       request.session[session_key] = True
   x=topic.posts.count()
   y=math.ceil(x/2)
   queryset=topic.posts.order_by('-created_at')

   page = request.GET.get('page', 1)
   paginator = Paginator(queryset, 2)
   try:
       topics = paginator.page(page)
   except PageNotAnInteger:
       topics = paginator.page(1)
   except EmptyPage:
       topics = paginator.page(paginator.num_pages)

   return render(request,'topic_posts.html',{'topics':topics , 'topic':topic,'y':y})

@login_required()
def reply_topic(request,pk,topic_pk):
    topic=get_object_or_404(Topic,board__pk=pk,pk=topic_pk)
    if request.method == 'POST':
        form=PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.topic=topic
            post.created_by=request.user
            post.save()
            topic.last_updated=timezone.now()
            topic.save()
            return redirect('topic_posts',pk=pk,topic_pk=topic_pk)

    else:
        form=PostForm()
        return render(request,'reply_topic.html',{'topic':topic,'form':form})


@method_decorator(login_required,name='dispatch')
class PostUpdateView(UpdateView):
    model=Post
    fields=('message',)
    template_name='edit_post.html'
    pk_url_kwarg='post_pk'
    context_object_name='post'

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self,form):
        post=form.save(commit=False)
        post.updated_by=self.request.user
        post.updated_at=timezone.now()
        post.save()
        return redirect('topic_posts',pk=post.topic.board.pk,topic_pk=post.topic.pk)


# Create your views here.
