from __future__ import unicode_literals

from django.apps import AppConfig
from django.conf import settings

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl.exceptions import NotFoundError

from .search import Book


class BooksConfig(AppConfig):
    name = 'books'

    def ready(self):
        connections.configure(default=settings.ES_CONNECTION)

        try:
            Book._doc_type.refresh()
        except NotFoundError:
            pass
