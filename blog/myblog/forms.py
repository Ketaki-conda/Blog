from django import forms
from .models import Post,Comment,Topic
from subscribe.models import SubscribeModel
from django.core.mail import EmailMessage
from django.template.loader import render_to_string, get_template
from blog.settings import EMAIL_HOST_USER


class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','author','image','body','isFeatured','topic')
        widgets={
        'title': forms.TextInput(attrs={'class':'sub-form-field mb-3'}),
        'author': forms.Select(attrs={'class':'sub-form-field mb-3'}),
        'body': forms.Textarea(attrs={'class':'sub-form-field mb-3'}),
        'topic':forms.Select(attrs={'class':'sub-form-field mb-3'})
        }
    def send_mail(self):
        a = Post.objects.order_by('-id')[0]
        b = SubscribeModel.objects.all()
        to = []
        for i in b:
            to.append(i.email)
        subject = "Check out our new blog \" " + self['title'].value() + "\""
        bodytext = self['body'].value()[:300]
        body_html = render_to_string(
            'mail_template.html',
            context={
                **{'id':a.id+1},
                **{'body':bodytext},
                **{'title':self['title'].value()},
            }
            
        )
        msg = EmailMessage(subject,body_html,EMAIL_HOST_USER,to)
        
        msg.content_subtype = "html"
        msg.send(fail_silently=False)



class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','body')
        widgets={
        'name': forms.TextInput(attrs={'class':'sub-form-field mb-3','placeholder':'Name'}),
        'body': forms.Textarea(attrs={'class':'sub-form-field mb-3','placeholder':'Enter Your Comment Here.  '}),

        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('topic_name','icon')
        widgets={
        'topic_name': forms.TextInput(attrs={'class':'sub-form-field mb-3'}),
        'icon': forms.TextInput(attrs={'class':'sub-form-field mb-3'}),
        }