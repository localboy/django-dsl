from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models import signals
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _

from elasticsearch_dsl.connections import connections

connections.create_connection(hosts=['localhost'], timeout=20)

from .managers import UserManager


class Author(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=200)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    class Meta:
        db_table = u'Author'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return u"Email: {}".format(self.email)

    def get_full_name(self):
        """ Returns the full name """
        name = u"{} {}".format(self.name)
        return name.strip()

    def get_short_name(self):
        return u"{}".format(self.email)

    def to_search(self):
        return {
            'name': self.name,
            'email': self.email
        }


class Book(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(unique=True, max_length=200)
    description = models.CharField(max_length=500)

    def to_search(self):
        return {
            'author': self.author.to_search(),
            'title': self.title,
            'description': self.description
        }


# def save_object_to_elastic_search(instance, created, **kwargs):
#     doc_type = str(instance._meta)
#     id = instance.id
#     data = model_to_dict(instance)
#
#     if created:
#         print 'Instance created'
#         print data
#         connections.get_connection().index(
#             doc_type=doc_type,
#             id=id,
#             body=data,
#         )
#     else:
#         connections.get_connection().update(
#             doc_type=doc_type,
#             id=id,
#             body=dict(
#                 doc=data,
#             ),
#         )
#
# signals.post_save.connect(save_object_to_elastic_search, sender=Book)