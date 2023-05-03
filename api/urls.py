from api import views
from django.conf.urls import url,include
from api.views import topic, news



urlpatterns = [
    url(r'^login/', views.LoginView.as_view()),
    url(r'^message/', views.MessageView.as_view()),
    # 获取临时密钥
    url(r'^credential/', views.CredentialView.as_view()),

    # 话题
    url(r'^topic/$', topic.TopicView.as_view()),
    url(r'^news/$', news.NewsView.as_view()),
    url(r'^news/(?P<pk>\d+)/$', news.NewsDetailView.as_view()),
]
