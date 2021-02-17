from django.urls import path,include
from .views import HomeView,ArticleDetailView,AddPostView,UpdatePostView, DeletePostView,AddCommentView,AddTopicView
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('article/<int:pk>',ArticleDetailView.as_view(),name='article-detail'),
    path('add_post/',AddPostView.as_view(), name='add_post'),
    path('add_topic/',AddTopicView.as_view(), name='add_topic'),
    path('article/edit/<int:pk>',UpdatePostView.as_view(),name='update_post'),
    path('article/<int:pk>/remove',DeletePostView.as_view(),name='delete_post'),
    path('like/<int:pk>', views.postLike, name='blog_like'),
    path('article/<int:pk>/comment/',AddCommentView.as_view(), name='add_comment'),
    path('subscribe/', include('subscribe.urls')),




]
