
from django.contrib import admin
from django.urls import path
from vimacon import views as vimaconviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vimacon/new-message/', vimaconviews.MessageCreateAPIView.as_view(), name='new-message'),

]
