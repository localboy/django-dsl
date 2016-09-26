from django.conf.urls import url

from .views import BooksList

urlpatterns = [
    url(r'^$', BooksList.as_view())
]