from __future__ import print_function

import sys
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from elasticsearch.helpers import streaming_bulk
from elasticsearch_dsl.connections import connections

from books.search import index
from books.models import Book


class Command(BaseCommand):
    # help = 'Indexing Data'

    def handle(self, *args, **kwargs):
        self.es = connections.get_connection()
        index.delete(ignore=404)
        index.create()
        self.verbose_run(Book)

    def verbose_run(self, model, report_every=100):
        name = model._meta.verbose_name

        print('Indexing %s: ' % name, end='')
        start = time.time()
        cnt = 0

        for _ in streaming_bulk(
                self.es,
                (m.to_search() for m in model.objects.all().iterator()),
                index=settings.ES_INDEX,
                doc_type=name.lower(),
        ):
            cnt += 1
            if cnt % report_every:
                print('.', end='')
                sys.stdout.flush()

        print('DONE\nIndexing %d %s in %.2f seconds' % (
            cnt, name, time.time() - start
        ))
