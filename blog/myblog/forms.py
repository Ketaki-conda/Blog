from django import forms
from .models import Post,Comment,Topic

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','author','image','body','isFeatured','topic')
        widgets={
        'title': forms.TextInput(attrs={'class':'form-control'}),
        'author': forms.Select(attrs={'class':'form-control'}),
        'body': forms.Textarea(attrs={'class':'form-control'}),
        'topic':forms.Select(attrs={'class':'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name','body')
        widgets={
        'name': forms.TextInput(attrs={'class':'form-control'}),
        'body': forms.Textarea(attrs={'class':'form-control'}),

        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('topic_name','icon')
        widgets={
        'topic_name': forms.TextInput(attrs={'class':'form-control'}),
        'icon': forms.TextInput(attrs={'class':'form-control'}),
        }