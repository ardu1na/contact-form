
from django.contrib import admin
from django.urls import path, include, re_path
from vimacon import views as vimaconviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vimacon/new-message/', vimaconviews.MessageCreateAPIView.as_view(), name='new-message'),
    path('api/vimacon/', include('vimacon.urls'), name="inbox"),
    re_path('api/vimacon/login', vimaconviews.login),
    re_path('api/vimacon/logout', vimaconviews.LogoutView.as_view()),

]
