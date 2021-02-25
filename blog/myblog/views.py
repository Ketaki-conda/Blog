from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView,View,FormView
from subscribe.models import  SubscribeModel     
from blog.settings import EMAIL_HOST_USER       
from .models import Post,Comment,IpModel,Topic
from .forms import PostForm,CommentForm,TopicForm
from subscribe.forms import Subscribe
from django.urls import reverse_lazy
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from django.core.mail import send_mail
import datetime
import random

class HomeView(View):
    template_name="home.html"

    def get(self,request):
        newposts = Post.objects.all().order_by('-id')[:4]
        sub = Subscribe()
        topics = Topic.objects.all()
        trending = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        featured = Post.objects.filter(isFeatured=True).order_by('-id')[:4]
        r = Post.objects.all()
        randomblog = r[random.randint(0,len(r)-1)]
        context = {
            **{'newposts':newposts},
            **{'topics':topics},
            **{'trending':trending},
            **{'featured':featured},
            **{'random':randomblog},
            **{'form1':sub}
        }
        return render(request,self.template_name,context)
    
    def post(self,request):
        if request.method == 'POST':
            sub = Subscribe(request.POST)
            if(sub.is_valid()):
                a = SubscribeModel(email = str(sub['Email'].value()),created_date = datetime.datetime.now())
                a.save()
                subject = 'Welcome to OurBlog'
                message = 'We are blessed to serve you!'
                recepient = str(sub['Email'].value())
                send_mail(subject,
                    message, EMAIL_HOST_USER, [recepient], fail_silently = False)
                return render(request, 'subscribe/success.html', {'recepient': recepient})
            else:
                return redirect('home')
        else:
            return redirect('home')

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
        topics = Topic.objects.all()
        sub = Subscribe()
        form = CommentForm()
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
        context['topics'] = topics
        context['form1'] = sub
        context['form'] = form

        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            sub = Subscribe(request.POST)
            form = CommentForm(request.POST)
            if(sub.is_valid()):
                a = SubscribeModel(email = str(sub['Email'].value()),created_date = datetime.datetime.now())
                a.save()
                subject = 'Welcome to OurBlog'
                message = 'We are blessed to serve you!'
                recepient = str(sub['Email'].value())
                send_mail(subject,
                    message, EMAIL_HOST_USER, [recepient], fail_silently = False)
                return HttpResponseRedirect(self.request.path_info)
            if(form.is_valid()):
                b = Comment(body = str(form['body'].value()),name = str(form['name'].value()),date_added = datetime.datetime.now(),post = get_object_or_404(Post,pk=kwargs['pk']))
                b.save()
                return HttpResponseRedirect(self.request.path_info)
            else:
                return redirect('home')
        else:
            return redirect('home')

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
    form_class = PostForm
    template_name="update_post.html"

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
