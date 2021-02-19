from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView,View,FormView            
from .models import Post,Comment,IpModel,Topic
from .forms import PostForm,CommentForm,TopicForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count


class HomeView(View):
    template_name="home.html"

    def get(self,request):
        newposts = Post.objects.all().order_by('post_date').order_by('-id')[:4]
        topics = Topic.objects.all()
        trending = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        featured = Post.objects.filter(isFeatured=True).order_by('-id')
        context = {
            **{'newposts':newposts},
            **{'topics':topics},
            **{'trending':trending},
            **{'featured':featured},
        }
        return render(request,self.template_name,context)

def get_client_ip(request):
    x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip=x_forwarded_for.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    return ip

class ArticleDetailView(DetailView):
    model=Post
    context_object_name='post'
    template_name="article_details.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        like_status=False
        ip=get_client_ip(request)
        if not IpModel.objects.filter(ip=ip).exists():
            IpModel.objects.create(ip=ip)
        if self.object.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
            like_status=True
        else:
            like_status=False
        context['like_status']=like_status

        return self.render_to_response(context)

class AddPostView(CreateView):
    model=Post
    form_class=PostForm
    template_name="add_post.html"

    def form_valid(self ,form):
        form.send_mail()
        return super().form_valid(form)


class AddTopicView(CreateView):
    model=Topic
    form_class=TopicForm
    template_name="add_topic.html"

class UpdatePostView(UpdateView):
    model=Post
    template_name="update_post.html"
    fields=['title', 'body','image','isFeatured']

class DeletePostView(DeleteView):
    model=Post
    template_name="delete_post.html"
    success_url=reverse_lazy('home')

class AddCommentView(CreateView):
    model=Comment
    form_class=CommentForm
    template_name="add_comment.html"

    def form_valid(self,form):
        form.instance.post_id=self.kwargs['pk']
        return super().form_valid(form)

    success_url=reverse_lazy('home')



def postLike(request,pk):
    post_id=request.POST.get('blog-id')
    post=Post.objects.get(pk=post_id)
    ip=get_client_ip(request)
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    if post.likes.filter(id=IpModel.objects.get(ip=ip).id).exists():
        post.likes.remove(IpModel.objects.get(ip=ip))
    else:
        post.likes.add(IpModel.objects.get(ip=ip))
    return HttpResponseRedirect(reverse('article-detail', args=[post_id]))
