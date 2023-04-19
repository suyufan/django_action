from api import views
from django.conf.urls import url,include


urlpatterns = [
    url(r'^login/', views.LoginView.as_view()),
    url(r'^message/', views.MessageView.as_view())
]
