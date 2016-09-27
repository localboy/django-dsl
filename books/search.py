from django.conf import settings

from elasticsearch_dsl import DocType, analyzer, String, Index, tokenizer, Object
from elasticsearch_dsl.connections import connections
connections.configure(
    default=settings.ES_CONNECTIONS
)

# Create custom Analyzer
my_analyzer = analyzer('my_analyzer',
                       tokenizer=tokenizer('trigram', 'nGram', min_gram=3, max_gram=3),
                       filter=['lowercase']
                       )

html_strip = analyzer('html_strip',
    tokenizer="standard",
    filter=["standard", "lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)

author_field = Object(properties={
    'display_name': String(fields={'raw': String(analyzer=my_analyzer, multi=True)})
})


class Book(DocType):
    author = author_field
    title = String(analyzer=my_analyzer, multi=True)

index = Index(settings.ES_INDEX)
index.doc_type(Book)
