from django.conf.urls import url

from .views import BooksList, SearchBooks

urlpatterns = [
    url(r'^/search/$', SearchBooks.as_view()),
    url(r'^$', BooksList.as_view())
]